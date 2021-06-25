from django.urls import path
from .views import *
from . import views
app_name = 'store'


urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('checkout', CheckoutView.as_view(), name='checkout-page'),
    path('add-cart/<slug>', views.add_to_cart, name='add-cart'),
    path('cart', CartFunc.as_view(), name='cart-page'),
    path('remove-cart/<slug>', views.remove_from_cart, name='remove-cart'),
    path('products', Product.as_view(), name='products-list'),
    path('product_detail/<slug>', ProductDetails.as_view(), name='product-detail'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single'),
    path('payment', views.payment, name='payment-page'),
    path('about-us', views.about_us, name='about-us'),
    path('contact-us', views.contact_us, name='contact-us'),
    path('blogs', views.blogs, name='blogs'),
    path('terms', views.terms, name='terms'),
    path('search', views.search, name='search'),
    #path('oauth/', 'social_django.urls', name='social'),
]

