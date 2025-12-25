import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    release_date__year__gte = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gte')
    release_date__year__lte = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lte')

    class Meta:
        model = Movie
        fields = ['genres', 'director', 'type', 'release_date__year__gte', 'release_date__year__lte']
