from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from apps.movies.models import Movie, MovieRate, UserToken
from apps.movies.choices import movie_genre, movie_rating


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]

        label = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Password Confirmation',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class MoviesForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'duration',
            'poster',
            'detail',
            'trailer_url',
            'genre',
            'original_language',
            'release_date',
            'country',
            'directors',
            'actors'
        ]

        labels = {
            'title': 'Title',
            'duration': 'Duration',
            'poster': 'Poster',
            'detail': 'Detail',
            'trailer_url': 'Trailer url',
            'genre': 'Genre',
            'original_language': 'Original language',
            'release_date': 'Release Date',
            'country': 'Country',
            'directors': 'Directors',
            'actors': 'Actors'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'genre': forms.Select(choices=movie_genre, attrs={'class': 'form-control'}),
            'original_language': forms.Select(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'directors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class RatingMoviesForm(forms.ModelForm):
    class Meta:
        model = MovieRate
        fields = [
            'movie',
            'rating',
            'comment'
        ]

        labels = {
            'movie': 'Movie',
            'rating': 'Rating',
            'comment': 'Comment'
        }

        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(choices=movie_rating, attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserTokenForm(forms.ModelForm):
    class Meta:
        model = UserToken
        fields = [
            'user',
        ]


class QueryMovieForm(forms.Form):
    query = forms.CharField(max_length=40)
