from django.contrib import admin
from .models import *


admin.site.register(Items)
admin.site.register(Order)
#admin.site.register(ShoppingCart)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customer)
