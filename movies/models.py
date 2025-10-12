from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration_minutes = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    director = models.ForeignKey(
        "Director", 
        on_delete=models.SET_NULL,  # když režiséra smažeš, film zůstane, ale bez režiséra
        null=True, 
        blank=True,
        related_name="movies"
    )

    def __str__(self):
        return self.title