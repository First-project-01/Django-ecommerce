import django_filters
from django_filters.filters import MultipleChoiceFilter, RangeFilter
from .models import Items

SIZES = (
    ('0', 'King - 108 x 120'),
    ('1', 'Queen - 90 x 108')
)

class ProductFilter(django_filters.FilterSet):
    size = MultipleChoiceFilter(choices=SIZES, null_label='Any', null_value='')
    price = RangeFilter()
    class Meta:
        model = Items
        fields = ['price', 'size', 'available']
