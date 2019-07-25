from django.contrib import admin
from .models import Movie, MovieActor, MovieDirector, Country, Genre, Language, MovieRate, UserToken

admin.site.register(Movie)
admin.site.register(MovieActor)
admin.site.register(MovieDirector)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(MovieRate)
admin.site.register(UserToken)