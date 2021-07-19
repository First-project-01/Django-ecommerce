from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegisterForm, CheckoutForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import *
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .filters import ProductFilter
from django.conf import settings
from django.http import HttpResponseRedirect

ID = settings.RAZORPAY_API_KEY_PUBLISHABLE
KEY = settings.RAZORPAY_API_KEY_HIDDEN
client = razorpay.Client(auth=(ID, KEY))
client.set_app_details({"title" : "AHD", "version" : "<YOUR_APP_VERSION>"})
    

class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'


class HomeView(ListView):
    context_object_name = 'items'
    template_name = "index.html"
    queryset = Items.objects.filter(featured=True)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['banners'] = Banner.objects.all()
        context['profile'] = Profile.objects.all()
        return context


class Product(ListView):
    model = Items
    paginate_by = 6
    template_name = 'products.html'
    ordering = ["-id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ProductFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = ProductFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context


class ProductDetails(DetailView):
    model = Items
    template_name = 'product-details.html' 


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_address': shipping_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect(reverse('store:cart-page'))

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default = form.cleaned_data.get(
                    'use_default')
                if use_default:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('store:checkout-page')
                else:
                    address = form.cleaned_data.get(
                        'address')
                    pincode = form.cleaned_data.get('zip')
                    phone = form.cleaned_data.get('phone')
                    city = form.cleaned_data.get('city')
                    state = form.cleaned_data.get('state')
                    if form.is_valid():
                        shipping_address = Address(
                            user=self.request.user,
                            address=address,
                            pincode=pincode,
                            state=state,
                            city=city,
                            phone=phone
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default = form.cleaned_data.get(
                            'set_default')
                        if set_default:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                    currency = 'INR'
                    amount = amount = int(order.get_total() * 100)  # Rs. 200
                    razorpay_order = client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
                    razorpay_order_id = razorpay_order['id']
                    callback_url = 'paymenthandler/'

                    # we need to pass these details to frontend.
                    context = {}
                    context['razorpay_order_id'] = razorpay_order_id
                    context['razorpay_merchant_key'] = ID
                    context['razorpay_amount'] = amount
                    context['currency'] = currency
                    context['callback_url'] = callback_url
                    return HttpResponseRedirect(reverse('store:checkout-page', kwargs={"context":context}))

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect(reverse('store:cart-page'))         


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        order = Cart.objects.get(user=request.user, ordered=False)
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = int(order.get_total() * 100)  # Rs. 200
                try:
                    # capture the payemt
                    client.payment.capture(payment_id, amount)
                    order.ordered = True
                    # render success page on successful caputre of payment
                    return render(request, 'paymentstatus.html')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'paymentstatus.html')
            else:
  
                # if signature verification fails.
                return render(request, 'paymentstatus.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect(reverse('store:home-page'))
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class CartFunc(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return render(self.request, 'cart.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=item,
        user=request.user,
        ordered=False
    )
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect(reverse('store:cart-page'))
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect(reverse('store:cart-page'))
    else:
        order = Cart.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect(reverse('store:cart-page'))


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect(reverse('store:cart-page'))
        else:  # change
            messages.info(request, "This item was not in your cart")
            return redirect(reverse('store:cart-page'))
    else:
        messages.info(request, "You do not have an active order")
        return redirect(reverse('store:cart-page'))


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order/cart
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect(reverse('store:cart-page'))
        else:
            messages.info(request, "This item was not in your cart")
            return redirect(reverse('store:cart-page'))
    else:
        messages.info(request, "You do not have an active order")
        return redirect(reverse('store:cart-page'))

 
class Wishlist(LoginRequiredMixin, View):
    paginate_by = 6
    def get(self, *args, **kwargs):
            products = Items.objects.filter(wishlist=self.request.user)
            context = {
                'wishlist': products
            }
            return render(self.request, 'wishlist.html', context)  


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Items, id=id)
    if product.wishlist.filter(id=request.user.id).exists():
        product.wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your wishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class OrderHistory(LoginRequiredMixin, View):
    paginate_by = 6
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=True)
            context = {
                'object': order
            }
            return render(self.request, 'order_history.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any placed orders")
            return render(self.request, 'order_history.html')  


def about_us(request):
    return render(request, 'about-us.html')


def contact_us(request):
    return render(request, 'contact.html')


def terms(request):
    return render(request, 'terms.html')

