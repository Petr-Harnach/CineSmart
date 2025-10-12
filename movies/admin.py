from django.contrib import admin
from .models import Movie, Genre, Director


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'get_genres', 'director')  # přidáme režiséra
    list_filter = ('genres', 'director')  # možnost filtrovat podle žánru a režiséra
    search_fields = ('title', 'description', 'director__name')  # vyhledávání podle názvu, popisu i režiséra

    def get_genres(self, obj):
        return ", ".join([g.name for g in obj.genres.all()])
    get_genres.short_description = 'Genres'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)