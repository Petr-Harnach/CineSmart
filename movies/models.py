from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='director_photos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='actor_photos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    MOVIE_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    country = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=10, choices=MOVIE_TYPE_CHOICES, default='movie')
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    trailer_url = models.URLField(blank=True)
    
    genres = models.ManyToManyField(Genre, related_name="movies")
    director = models.ForeignKey(
        "Director", 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name="movies"
    )
    screenwriter = models.CharField(max_length=150, blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    def __str__(self):
        return self.title


class WatchlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist'
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='watchlist_items'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'Review for {self.movie.title} by {self.user.username}'


class ReviewLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_likes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f'{self.user.username} likes {self.review.id}'


    

    