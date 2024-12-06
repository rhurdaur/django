from django.db import models
from django.views.decorators.cache import cache_page
from django.conf import settings


class DateTimeMixin(models.Model):
    """abstrakte Klassen erzeugen keine DB-Tabelle."""

    created_at = models.DateTimeField(auto_now_add=True)  # wir bei Create eingetragen
    updated_at = models.DateTimeField(auto_now=True)  # wird bei Update upgedated

    class Meta:
        abstract = True


class CacheMixin:
    cache_timeout = settings.CACHE_TIMEOUT

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *a, **k):
        return cache_page(self.get_cache_timeout())(super().dispatch)(*a, **k)
