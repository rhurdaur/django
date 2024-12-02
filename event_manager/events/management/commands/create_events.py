""" 
Sub-kommando um Kategorien und Events zu erstellen.
Argparser nutzen.

python manage.py create_events --events 100
"""
import random
from django.core.management.base import BaseCommand
from events.models import Category, Event 
from events.factories import CategoryFactory, EventFactory

NUM_CATEGORIES = 10


class Command(BaseCommand):
    def add_arguments(self, parser):
        """Argument-Vektor auslesen"""
        parser.description = "Generate n random events"
        parser.add_argument(
            "-e",
            "--events",
            type=int,
            required=True
        )
        parser.epilog = "Nutzung: python manage.py create_events --events 100"

    def handle(self, *args, **options):
        n = options.get("events")
        categories = CategoryFactory.create_batch(NUM_CATEGORIES)
        events = EventFactory.create_batch(n)
        # Alternative: Kategorie-Objekt via Instantiierung übergeben
        # for _ in range(20):
        #     EventFactory(category=random.choice(categories))