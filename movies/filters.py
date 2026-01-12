import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    release_date__year__gte = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gte')
    release_date__year__lte = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lte')
    release_date__gte = django_filters.DateFilter(field_name='release_date', lookup_expr='gte')
    release_date__lte = django_filters.DateFilter(field_name='release_date', lookup_expr='lte')
    release_date__gt = django_filters.DateFilter(field_name='release_date', lookup_expr='gt')

    class Meta:
        model = Movie
        fields = ['genres', 'director', 'type', 'release_date__year__gte', 'release_date__year__lte']
