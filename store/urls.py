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
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_wishlist/<int:id>", views.add_to_wishlist, name="add_wishlist"),
    path('order_history', views.order_history, name='order_history'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-single'),
    path('about-us', views.about_us, name='about-us'),
    path('contact-us', views.contact_us, name='contact-us'),
    path('terms', views.terms, name='terms'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
    #path('oauth/', 'social_django.urls', name='social'),
]

