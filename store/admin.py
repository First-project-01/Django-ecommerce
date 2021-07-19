from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'ordered_date',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
    ]
    list_filter = ['ordered',
                   'ordered_date',
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


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone',
    ]
    list_display_links = [
        'user',
    ]


admin.site.register(Items)
admin.site.register(Banner)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem)
admin.site.register(Address, AddressAdmin)
admin.site.register(Profile, ProfileAdmin)
