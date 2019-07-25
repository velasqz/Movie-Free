from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from apps.movies.models import Movie


@receiver(pre_save, sender=Movie)
def create_slug_for_movie(instance, **kwargs):
    instance.slug = slugify(instance.title)
    return instance