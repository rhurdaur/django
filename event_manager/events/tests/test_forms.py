from datetime import timedelta

from unittest import skip
from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.forms.models import model_to_dict

from events.factories import CategoryFactory, EventFactory
from user.factories import UserFactory
from events.models import Category, Event


def get_author(moderator=False):
    return UserFactory()


def show_form_errors(response) -> None:
    """Show Form Errors from response context."""

    if isinstance(response.context, dict) and "form" in response.context:
        form = response.context["form"]

        # Check if the form has errors
        if form.errors:
            print("Form Errors:", form.errors)

            # For a more detailed output, iterate through the errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field '{field}': {error}")
        else:
            print("No form errors found.")
    else:
        print("Form is not in the context.")


class EventFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_author()
        cls.category = CategoryFactory()  # Category.objects.create(name=xy)

    def setUp(self):
        self.client = Client()  ## anonymer ouser
        self.payload = {
            "name": "Test Event",
            "sub_title": "test sub",
            "description": "test desc",
            "date": timezone.now() + timedelta(hours=3),
            "category": self.category.pk,
            "min_group": 10,
        }

    def test_create_event_successful(self):
        self.client.force_login(self.author)

        # GET
        response = self.client.get(reverse("events:event_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/event_form.html")

        # POST
        response = self.client.post(reverse("events:event_create"), data=self.payload)
        show_form_errors(response)
        self.assertEqual(response.status_code, 302)
        last = Event.objects.last()
        self.assertEqual(last.name, self.payload.get("name"))
        self.assertRedirects(
            response,
            reverse("events:event_detail", args=(last.pk,)),
            target_status_code=200,
        )

    def test_edit_event_successful(self):
        self.client.force_login(self.author)
        event = EventFactory(author=self.author)
        payload = model_to_dict(event)
        payload["name"] = "Updated Name"

        # POST
        response = self.client.post(
            reverse("events:event_update", args=(event.pk,)),
            payload,
        )
        self.assertEqual(response.status_code, 302)
        events = Event.objects.filter(name=payload["name"])
        self.assertTrue(events)

    def test_cannot_edit_event_from_other_user(self):
        self.client.force_login(self.author)
        event = EventFactory()
        payload = model_to_dict(event)
        response = self.client.post(
            reverse("events:event_update", args=(event.pk,)),
            payload,
        )
        self.assertEqual(response.status_code, 403)


class CategoryFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """wird einmalig für alle Tests der Klasse ausgeführt."""

        cls.category = CategoryFactory()

    def setUp(self):
        self.client = Client()
        self.payload = {
            "name": "Valid Category Name",
            "sub_title": "Valid Subtitle",
            "description": "valid something",
        }

    def test_create_category_successful(self):
        """Prüfen, ob eine Kategorie erfolgreich angelegt werden kann."""

        # GET Request prüfen
        response = self.client.get(reverse("events:category_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/category_form.html")

        # POST Request
        response = self.client.post(reverse("events:category_create"), self.payload)

        self.assertEqual(response.status_code, 302)
        last = Category.objects.last()
        self.assertEqual(last.name, self.payload.get("name"))
        self.assertRedirects(
            response,
            reverse("events:category_detail", args=(last.pk,)),
            target_status_code=200,
        )
