""" 
Sub-kommando um Kategorien und Events zu erstellen.
Argparser nutzen.

python manage.py create_events --events 100
"""

import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from events.models import Category, Event, Ticket, Review
from events.factories import CategoryFactory, EventFactory, ReviewFactory

NUM_CATEGORIES = 10


class Command(BaseCommand):
    def add_arguments(self, parser):
        """Argument-Vektor auslesen"""
        parser.description = "Generate n random events"
        parser.add_argument("-e", "--events", type=int, required=True)
        parser.epilog = "Nutzung: python manage.py create_events --events 100"

    def handle(self, *args, **options):
        n = options.get("events")

        print("Delete everything.")
        for model in [Ticket, Review, Event, Category]:
            model.objects.all().delete()

        print("Create events...")
        categories = CategoryFactory.create_batch(NUM_CATEGORIES)
        events = EventFactory.create_batch(n)
        user_list = get_user_model().objects.all()

        print("Create reviews...")
        for user in user_list:
            for _ in range(random.randint(1, 6)):
                ReviewFactory(
                    author=user,
                    event=random.choice(events),
                )
