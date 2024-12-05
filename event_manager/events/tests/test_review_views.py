""" 
Testen der Review Views.

- Anlegen eines Reviews via POST

weitere Tests, die implementiert werden müssen

- Testen, dass nicht-authentifizierter User keinen Test anlegen kann
- Testen, dass der review_text entweder leer, oder min. 10 Zeichen lang ist
- Testen, dass kein Review erstellt wird, wenn kein Event übergeben wird


"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from events.factories import CategoryFactory, EventFactory, ReviewFactory
from user.factories import UserFactory
from events.models import Review, Event
from .test_helpers import show_form_errors

User = get_user_model()


class ReviewViewTest(TestCase):
    def setUp(self):
        self.event = EventFactory()
        self.author = UserFactory()
        self.client = Client()
        self.client.force_login(self.author)

        self.payload = {
            "name": "Toller Event",
            "review_text": "Some Review Text",
            "rating": 5,
        }

    def test_review_create_with_valid_payload(self):
        # 20 Minuten Zeit, View implementieren
        response = self.client.post(
            reverse("events:review_create", args=(self.event.pk,)),
            self.payload,
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().review_text, "Some Review Text")

    def test_create_review_with_empty_text(self):
        """Review text can be empty."""
        self.payload["review_text"] = ""
        response = self.client.post(
            reverse("events:review_create", args=(self.event.pk,)),
            self.payload,
        )
        self.assertEqual(response.status_code, 302)  # Redirect to event detail
        self.assertEqual(Review.objects.count(), 1)  # Review created successfully
        review = Review.objects.first()
        self.assertEqual(review.review_text, "")  # Review text is empty

    def test_create_review_with_invalid_text(self):
        """Review text shorter than 10 characters should fail."""
        self.payload["review_text"] = "abcde3434"

        response = self.client.post(
            reverse("events:review_create", args=(self.event.pk,)),
            self.payload,
        )
        self.assertEqual(response.status_code, 200)  # Form reloaded with errors
        self.assertEqual(Review.objects.count(), 0)  # No review created
        self.assertContains(
            response, "The review text must be at least 10 characters long or empty."
        )

    def test_create_review_as_unauthenticated_user(self):
        """Test that unauthenticated users cannot create reviews."""
        self.client.logout()  # Log out the user
        response = self.client.post(
            reverse("events:review_create", args=(self.event.pk,)),
            self.payload,
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertEqual(Review.objects.count(), 0)  # Review should not be created
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/events/review/create/{self.event.pk}",
            target_status_code=200,
        )
