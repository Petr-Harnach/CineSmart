from django.contrib import admin
from .models import Movie, Genre, Director, CustomUser, Review, Actor, Screenwriter, Season, Episode
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Screenwriter)
class ScreenwriterAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'movie', 'season_number', 'release_date')
    list_filter = ('movie',)
    search_fields = ('movie__title', 'title')
    inlines = [EpisodeInline]


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 0
    show_change_link = True # Allow clicking through to edit episodes


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'type', 'get_genres', 'get_directors')
    list_filter = ('type', 'genres', 'directors')
    search_fields = ('title', 'description', 'directors__name')
    filter_horizontal = ('genres', 'directors', 'actors', 'screenwriters')
    inlines = [SeasonInline] # Add seasons directly to movie

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])
    get_genres.short_description = 'Genres'

    def get_directors(self, obj):
        return ", ".join([d.name for d in obj.directors.all()])
    get_directors.short_description = 'Directors'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'comment')