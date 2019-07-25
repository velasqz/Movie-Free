from django.apps import AppConfig


class MoviesConfig(AppConfig):
    name = 'apps.movies'
    verbose_name = 'Django Movie Database'

    def ready(self):
        import apps.movies.signals