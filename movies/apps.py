from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        # Removed: import movies.signals
        pass # Add a pass statement since ready() needs some content if not importing signals