from django.urls import path
from . import views
app_name = 'store'


urlpatterns = [
    path('', views.home, name='home-page'),
    path('/products', views.product, name='products-list'),
    path('/product_detail', views.productdetails, name='product-detail'),
]
