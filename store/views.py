from django.shortcuts import render
from .models import Items


def home(request):
    context = {
        'items': Items.objects.all()
    }
    return render(request, 'product.html', context)

