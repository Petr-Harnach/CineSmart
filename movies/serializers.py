from rest_framework import serializers
from .models import Movie, Genre, Director

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration_minutes', 'genres', 'director']
