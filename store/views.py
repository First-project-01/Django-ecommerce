from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
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
    model = Items.slug
    template_name =  'product-details.html'

def register(request):
    form = UserCreationForm()
    return render(request, 'login.html', {'form' : form})


def createuser(request):
    form = UserCreationForm()
    return render(request, 'login.html', {'form' : form})
