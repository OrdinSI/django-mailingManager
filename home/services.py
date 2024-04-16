from random import sample

from django.core.cache import cache
from config import settings


def get_post(model, cache_prefix=''):
    """Returns a list of model"""
    if settings.CACHE_ENABLED:
        queryset = cache.get(cache_prefix)
        if not queryset:
            queryset = list(model.objects.all())
            cache.set(cache_prefix, queryset)
        return sample(queryset, min(4, len(queryset)))
