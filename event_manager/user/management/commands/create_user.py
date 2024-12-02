"""
Eigenes Sub-Kommando zum Erstellen von Usern 

python manage.py create_user
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from user.factories import UserFactory


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Delete Users...")
        get_user_model().objects.exclude(username="admin").delete()
        print("Users deleted.")

        UserFactory.create_batch(6)