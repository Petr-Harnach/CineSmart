from rest_framework import serializers
from .models import Movie, Genre, Director, Review, Actor


# Vlastní pole pro generování absolutních URL pro obrázky
class AbsoluteImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(value.url)
        return value.url


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


# Zjednodušený serializer pro filmy v rámci profilu herce/režiséra
class BasicMovieSerializer(serializers.ModelSerializer):
    poster = AbsoluteImageField(read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster', 'release_date']


class DirectorSerializer(serializers.ModelSerializer):
    movies = BasicMovieSerializer(many=True, read_only=True)
    photo = AbsoluteImageField(read_only=True)
    class Meta:
        model = Director
        fields = ['id', 'name', 'bio', 'photo', 'movies']


class ActorSerializer(serializers.ModelSerializer):
    movies = BasicMovieSerializer(many=True, read_only=True)
    photo = AbsoluteImageField(read_only=True)
    class Meta:
        model = Actor
        fields = ['id', 'name', 'bio', 'photo', 'movies']


# Serializer pro přihlášeného uživatele (vlastní profil)
class MyProfileSerializer(serializers.ModelSerializer):
    profile_picture = AbsoluteImageField(read_only=True)
    class Meta:
        model = __import__('django').contrib.auth.get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']


class ReviewSerializer(serializers.ModelSerializer):
    user = MyProfileSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), write_only=True, source='movie'
    )
    comment = serializers.CharField(required=False, allow_blank=True)
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'user', 'movie_id', 'likes_count', 'user_has_liked']
        read_only_fields = ['created_at', 'user']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_user_has_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

    def create(self, validated_data):
        # Check if the user has already reviewed this movie
        user = self.context['request'].user
        movie = validated_data['movie']
        if Review.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError("You have already reviewed this movie.")
        return super().create(validated_data)


# Serializer pro veřejné profily ostatních uživatelů
class PublicUserSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    profile_picture = AbsoluteImageField(read_only=True)
    class Meta:
        model = __import__('django').contrib.auth.get_user_model()
        fields = ['id', 'username', 'bio', 'profile_picture', 'reviews']


class MovieSerializer(serializers.ModelSerializer):
    poster = AbsoluteImageField(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True, source='genres'
    )
    director_id = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(), write_only=True, source='director', allow_null=True
    )
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(), many=True, write_only=True, source='actors', required=False
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date', 'duration_minutes', 'country', 'type', 'poster', 'trailer_url',
            'genres', 'director', 'reviews', 'actors', 'screenwriter', 'avg_rating',
            'genre_ids', 'director_id', 'actor_ids'
        ]


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
        fields = ['id', 'movie', 'movie_id', 'added_at', 'watched']
