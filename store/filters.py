import django_filters
from .models import Items


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Items
        fields = ['size', 'category']
        '''filter_overrides = {models.BooleanField: {
                'filter_class': django_filters.BooleanFilter(),
                'extra': lambda f: {
                    widgets: forms.RadioInput,
                },
            }
        }'''
