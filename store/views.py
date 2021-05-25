from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import *


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
    return render (request, 'checkout.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('fullname')
            #messages.success(request, f'Account created for {username}!')
            return redirect(reverse('store:home-page'))
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def cart(request):
    item = OrderItem.objects.all()
    return render(request, 'cart.html', {'item': item})

def add_to_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("store:product-detail")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("store:product-detail")
    else:
        ordered_date = timezone.now()
        order = Cart.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("store:product-detail")


def remove_from_cart(request, slug):
    item = get_object_or_404(Items, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("store:product-detail")
        else:                                                           #change
            messages.info(request, "This item was not in your cart")
            return redirect("store:product-detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product-detail", slug=slug)

