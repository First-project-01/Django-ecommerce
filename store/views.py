from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import *
from django.http import HttpResponse


class HomeView(ListView):
    model = Items
    template_name = "index.html"


class Product(ListView):
    model = Items
    paginate_by = 10
    template_name = 'products.html'


class ProductDetails(DetailView):
    model = Items
    template_name = 'product-details.html'


def checkout(request):
    return render(request, 'checkout.html', {'title': 'Checkout'})


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