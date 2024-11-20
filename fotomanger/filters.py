from django.forms import DateInput
from django_filters import rest_framework as filters
from photologue.models import Photo

class PhotoFilter(filters.FilterSet):
    date_taken__gte = filters.DateTimeFilter(field_name="date_added", lookup_expr='date__gte',
                                             widget=DateInput(attrs={'type': 'date'}))
    date_taken__lte = filters.DateTimeFilter(field_name="date_added", lookup_expr='date__lte',
                                             widget=DateInput(attrs={'type': 'date'}))
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    slug = filters.CharFilter(field_name="slug", lookup_expr='icontains')
    # date_taken = filters.DateTimeFilter(field_name="date_added", lookup_expr='date', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Photo
        fields = [
            'date_taken__gte', 'date_taken__lte', 'title', 'slug',
            # 'date_taken',
        ]
