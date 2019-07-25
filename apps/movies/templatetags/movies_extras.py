from django import template
from apps.movies.models import MovieRate

register = template.Library()


@register.filter
def data(value):
    return value.all()


@register.filter
def url(value):
    try:
        if '=' in value:
            value = value.split('=')
            return value[1]
        else:
            return value
    except Exception:
        return value


@register.filter
def movie_rate(value):
    try:
        data = MovieRate.objects.filter(movie=value).get_best_rated()
        return data.first()['rate']
    except Exception:
        return ''
