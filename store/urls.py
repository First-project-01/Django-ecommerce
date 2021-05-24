from django.urls import path
from .views import *
from . import views
app_name = 'store'


urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('products', Product.as_view(), name='products-list'),
    path('product_detail/<slug>', ProductDetails.as_view(), name='product-detail'),
    path('register', views.register, name='register'),
]
