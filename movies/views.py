from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Genre, Director
from .serializers import MovieSerializer, GenreSerializer, DirectorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genres', 'director']  # filtrování podle žánru a režiséra
    search_fields = ['title', 'description']   # fulltext vyhledávání
    ordering_fields = ['release_date', 'title']  # možnost řazení


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
