from rest_framework import serializers
from .models import Movie, Genre, Director, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    # Read-only nested representation for GET
    genres = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)

    # Write-only fields for creating/updating relationships (accept PKs)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True, source='genres'
    )
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(), write_only=True, source='director', allow_null=True
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date', 'duration_minutes',
            'genres', 'genre_ids', 'director', 'director_id'
        ]

    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError("duration_minutes must be a positive integer.")
        return value

    # Add explicit help_text for OpenAPI generation and readability
    title = serializers.CharField(help_text='Movie title', max_length=200)
    description = serializers.CharField(help_text='Full description of the movie')
    release_date = serializers.DateField(help_text='Release date in YYYY-MM-DD format')
    duration_minutes = serializers.IntegerField(help_text='Duration in minutes')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = __import__('django').contrib.auth.get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = __import__('django').contrib.auth.get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        User = __import__('django').contrib.auth.get_user_model()
        user = User(username=validated_data['username'], email=validated_data.get('email', ''))
        user.set_password(validated_data['password'])
        user.save()
        return user


class WatchlistItemSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True, source='movie')

    class Meta:
        model = __import__('django').apps.apps.get_model('movies', 'WatchlistItem')
        fields = ['id', 'movie', 'movie_id', 'added_at']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), write_only=True, source='movie'
    )

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'user', 'movie_id']
        read_only_fields = ['created_at', 'user']

    def create(self, validated_data):
        # Check if the user has already reviewed this movie
        user = self.context['request'].user
        movie = validated_data['movie']
        if Review.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError("You have already reviewed this movie.")
        return super().create(validated_data)
