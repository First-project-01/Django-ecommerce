from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import *


class HomeView(ListView):
    model = Items
    template_name = "index.html"


class Product(ListView):
    model = Items
    paginate_by = 8
    template_name = 'products.html'


class ProductDetails(DetailView):
    context_object_name = 'items'
    template_name = 'product-details.html'
    queryset = Items.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        context['order-item'] = OrderItem.objects.all()
        return context


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
                    {'default_shipping_address': shipping_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("store:cart-page")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
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
                    address1 = form.cleaned_data.get(
                        'address')
                    pincode = form.cleaned_data.get('zip')
                    phone = form.cleaned_data.get('phone')
                    city = form.cleaned_data.get('city')
                    state = form.cleaned_data.get('state')
                    if form.is_valid():
                        shipping_address = Address(
                            user=self.request.user,
                            address=address1,
                            pincode=pincode,
                            state=state,
                            city=city,
                            phone=phone
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                payment_option = form.cleaned_data.get('payment')
                if payment_option == 'C':
                    return redirect('store:payment', payment_option='credit')
                elif payment_option == 'D':
                    return redirect('store:payment', payment_option='debit')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('store:checkout-page')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("store:cart-page")


#class Payment(View):


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect(reverse('login-page'))
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
            return redirect(reverse('store:home-page'))


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
        ordered_date = timezone.now()
        order = Cart.objects.create(user=request.user, ordered_date=ordered_date)
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
        else:                                                           #change
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
        # check if the order item is in the order
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

def about_us(request):
    return render(request, 'about-us.html')

def contact_us(request):
    return render(request, 'contact.html')

def blogs(request):
    return render(request, 'blog.html')

def terms(request):
    return render(request, 'terms.html')