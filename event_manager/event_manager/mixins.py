from django.db import models


class DateTimeMixin(models.Model):
    """abstrakte Klassen erzeugen keine DB-Tabelle."""
    created_at = models.DateTimeField(auto_now_add=True) # wir bei Create eingetragen
    updated_at = models.DateTimeField(auto_now=True)  # wird bei Update upgedated

    class Meta:
        abstract = True