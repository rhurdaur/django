import random

import factory 
from django.utils import timezone
from datetime import timedelta

from user.factories import UserFactory
from .models import Category, Event


categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)
    
    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=5, locale="de_DE")
    

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
    
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("sentence")
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=5, locale="de_DE")
    min_group = factory.LazyAttribute(
        lambda _: random.choice(Event.Group.values)
    )
    date = factory.Faker(
        "date_time_between",
        end_date=timezone.now() + timedelta(days=60),
        start_date=timezone.now() + timedelta(hours=1),
        tzinfo=timezone.get_current_timezone(),
    )
    
    