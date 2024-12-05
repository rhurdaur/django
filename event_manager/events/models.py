from functools import partial

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, RegexValidator
from event_manager.mixins import DateTimeMixin
from .validators import (
    datetime_in_future,
    validate_name,
    bad_word_filter,
    validate_review_text,
)

User = get_user_model()


class Review(DateTimeMixin):

    class Ratings(models.IntegerChoices):
        AWESOME = 6
        SUPER = 5
        GOOD = 4
        OK = 3
        BAD = 2
        WORST = 1

    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField(
        blank=True, null=True, validators=[validate_review_text]
    )
    rating = models.IntegerField(choices=Ratings.choices)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="tickets")
    nummer = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                r"^[a-zA-Z0-9]{8}$", "Nummer must be 8 alphanumeric characters"
            )
        ],
    )
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.nummer})"


class Category(DateTimeMixin):

    name = models.CharField(max_length=100, unique=True)
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(
        help_text=_("Beschreibung der Kategorie"), null=True, blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Kategorie")
        verbose_name_plural = _("Kategorien")

    def __str__(self) -> str:
        return self.name


class Event(DateTimeMixin):
    # thin view, fat model

    class Group(models.IntegerChoices):
        BIG = 10, _("mittelgroße Gruppe")
        SMALL = 2, _("sehr kleine Gruppe")
        LARGE = 20, _("große Gruppe")

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3), validate_name],
    )
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(
        help_text=_("Beschreibung des Events"),
        null=True,
        blank=True,
        validators=[
            partial(bad_word_filter, ["doof", "evil"]),
        ],
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(validators=[datetime_in_future])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    min_group = models.IntegerField(choices=Group.choices)

    def related_events(self):
        """Ähnliche Events auflisten."""
        related_events = Event.objects.filter(
            min_group=self.min_group, category=self.category
        )
        return related_events.exclude(pk=self.pk)

    def get_absolute_url(self):
        """Homepage zum Event."""
        return reverse("events:event_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name
