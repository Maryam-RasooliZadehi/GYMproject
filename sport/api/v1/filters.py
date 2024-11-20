from ...models import Plan , Diet
import django_filters

class PlanFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = {
            'course': ['exact'],
            'day_of_week':['iexact']
        }

class DietFilter(django_filters.FilterSet):
    class Meta:
        model= Diet
        fields= {
            'course' : ['exact']
        }
