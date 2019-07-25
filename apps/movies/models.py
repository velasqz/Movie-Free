from django.db import models
from django.conf import settings
from apps.movies.choices import movie_rating
from django.urls import reverse_lazy
import uuid

from apps.movies.queryset import MovieRateQueryset


def movie_directory_path(instance, filename):
    return f'movie/{instance.title}/{filename}'


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False)
    duration = models.IntegerField(null=False)
    poster = models.ImageField(upload_to=movie_directory_path, null=True)
    detail = models.TextField(null=False, max_length=500)
    trailer_url = models.URLField(null=True, blank=True)
    genre = models.CharField(max_length=30, null=False)
    original_language = models.ForeignKey('Language', null=True, on_delete=models.SET_NULL)
    release_date = models.DateField(null=True)
    country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)
    directors = models.ManyToManyField('MovieDirector')
    actors = models.ManyToManyField('MovieActor')
    slug = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('movie-detail', args=(self.title,))


class MovieRate(models.Model):
    movie = models.ForeignKey('Movie', null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(choices=movie_rating, null=False)
    comment = models.TextField(null=False, max_length=150)

    objects = MovieRateQueryset.as_manager()

    def __str__(self):
        return 'Movie: {}'.format(self.movie.title)


class MovieActor(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    age = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.name


class MovieDirector(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    age = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=15, unique=True, null=False)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name


class UserToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    token = models.UUIDField(default=uuid.uuid4)
