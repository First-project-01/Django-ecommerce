from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',
        'state',
        'pincode',
        'city',
        'default'
    ]
    list_filter = ['default', 'city', 'state']
    search_fields = ['user', 'address', 'pincode']


class ItemsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Items, ItemsAdmin)
admin.site.register(Banner)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem)
admin.site.register(Address, AddressAdmin)
admin.site.register(Profile)
