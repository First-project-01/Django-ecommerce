from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic import ListView, DetailView
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

