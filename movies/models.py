from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# --- CLOUDINARY IMPORT (Zakomentovat pro lokální vývoj bez Cloudinary) ---
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    # bio = models.TextField(blank=True) # REMOVED
    
    # --- IMAGE FIELDS (Přepínat mezi lokálem a produkcí) ---
    
    # LOCAL (Aktivní):
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # cover_picture = models.ImageField(upload_to='cover_pics/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    profile_picture = CloudinaryField('image', null=True, blank=True)
    cover_picture = CloudinaryField('image', null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=150, unique=True)
    # bio = models.TextField(blank=True) # REMOVED
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, blank=True)
    
    # LOCAL (Aktivní):
    # photo = models.ImageField(upload_to='director_photos/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    photo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name


class Screenwriter(models.Model):
    name = models.CharField(max_length=150, unique=True)
    # bio = models.TextField(blank=True) # REMOVED
    
    # LOCAL (Aktivní):
    # photo = models.ImageField(upload_to='screenwriter_photos/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    photo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=150, unique=True)
    # bio = models.TextField(blank=True) # REMOVED
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, blank=True)
    
    # LOCAL (Aktivní):
    # photo = models.ImageField(upload_to='actor_photos/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    photo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    MOVIE_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'Series'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True) # Optional
    release_date = models.DateField(null=True, blank=True) # Optional
    end_date = models.DateField(null=True, blank=True) # New field for series end date
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True) # Optional
    country = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=10, choices=MOVIE_TYPE_CHOICES, default='movie')
    
    # LOCAL (Aktivní):
    # poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    poster = CloudinaryField('image', null=True, blank=True)
    
    trailer_url = models.URLField(blank=True)
    
    genres = models.ManyToManyField(Genre, related_name="movies")
    
    # Main crew/cast for the whole show
    directors = models.ManyToManyField(Director, related_name="movies", blank=True)
    screenwriters = models.ManyToManyField(Screenwriter, related_name="movies", blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    def __str__(self):
        return self.title


class Season(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.IntegerField()
    title = models.CharField(max_length=200, blank=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    
    # Season poster
    # LOCAL (Aktivní):
    # poster = models.ImageField(upload_to='season_posters/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    poster = CloudinaryField('image', null=True, blank=True)

    # Season specific crew/cast (useful for anthologies)
    directors = models.ManyToManyField(Director, related_name='seasons', blank=True)
    screenwriters = models.ManyToManyField(Screenwriter, related_name='seasons', blank=True)
    actors = models.ManyToManyField(Actor, related_name='seasons', blank=True)
    
    class Meta:
        ordering = ['season_number']

    def __str__(self):
        return f"{self.movie.title} - Season {self.season_number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    overview = models.TextField(blank=True)
    air_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    
    # Episode specific crew/cast
    directors = models.ManyToManyField(Director, related_name='episodes', blank=True)
    screenwriters = models.ManyToManyField(Screenwriter, related_name='episodes', blank=True)
    guest_stars = models.ManyToManyField(Actor, related_name='episodes', blank=True)
    
    # LOCAL (Aktivní):
    # still_path = models.ImageField(upload_to='episode_stills/', null=True, blank=True)
    
    # PRODUCTION (Zakomentované):
    still_path = CloudinaryField('image', null=True, blank=True)

    class Meta:
        ordering = ['episode_number']

    def __str__(self):
        return f"{self.season.movie.title} - S{self.season.season_number}E{self.episode_number} - {self.title}"


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


class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"


class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='collection_items')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collection', 'movie')

    def __str__(self):
        return f"{self.movie.title} in {self.collection.name}"
