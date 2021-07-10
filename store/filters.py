import django_filters
from django_filters.filters import OrderingFilter, RangeFilter
from .models import Items

class ProductFilter(django_filters.FilterSet):
    sort = OrderingFilter(
        choices=(
            ('price', 'Lowest to Highest'),
            ('-price', 'Highest to Lowest'),
            ),
        label = 'Sort By'
    )
    class Meta:
        model = Items
        fields = ['size', 'category']


