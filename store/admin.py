from django.contrib import admin
from .models import Items, CartItems, ShoppingCart, Payment, Address, UserModel


admin.site.register(Items)
admin.site.register(CartItems)
admin.site.register(ShoppingCart)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(UserModel)
