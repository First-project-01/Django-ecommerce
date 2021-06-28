import django_filters
from django_filters.filters import OrderingFilter, RangeFilter
from .models import Items

class ProductFilter(django_filters.FilterSet):
    sort = OrderingFilter(
        choices=(
            ('-date_added', 'Latest products'),
            ('price', 'Lowest to Highest'),
            ('-price', 'Highest to Lowest'),
            ),
        fields={
            'price': 'price',
        },
    )
    price = RangeFilter()
    class Meta:
        model = Items
        fields = ['size', 'category']
