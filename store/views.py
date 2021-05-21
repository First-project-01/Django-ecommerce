from django.shortcuts import render
from .models import Items


context = {
        'items': Items.objects.all()
    }
def home(request):
    return render(request, 'index.html', context)


def product(request):
    return render(request, 'products.html', context)


def productdetails(request):
    return render(request, 'product-details.html', context)
