from django.shortcuts import render
from .models import Items


def home(request):
    return render(request, 'index.html')


def product(request):
    context = {
     'items': Items.objects.all()
    }
    return render(request, 'products.html', context)


def productdetails(request):
    context = {
     'items': Items.objects.all()
    }
    return render(request, 'product-details.html', context)
