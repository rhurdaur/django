from django.test import TestCase
from django.urls import reverse
from events.factories import CategoryFactory, EventFactory
from user.factories import UserFactory
from events.models import Category, Event, Ticket


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


class TicketTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = UserFactory()
        self.client.force_login(self.user)
        self.event = EventFactory()
        self.payload = {
            "name": "Test Ticket",
            "event": self.event.pk,
            "nummer": "A1B2C3D4",
            "message": "This is a test ticket.",
        }

    def test_create_ticket_success(self):
        # Create a valid ticket
        response = self.client.post(
            reverse("events:ticket_create"),
            self.payload,
        )
        show_form_errors(response)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.first().nummer, "A1B2C3D4")

    def test_invalid_ticket_number(self):
        # Try to create a ticket with an invalid number
        self.payload["nummer"] = "3"
        response = self.client.post(
            reverse("events:ticket_create"),
            self.payload,
        )
        self.assertEqual(response.status_code, 200)  # Form re-renders on error
        self.assertEqual(Ticket.objects.count(), 0)

    def test_duplicate_ticket_number(self):
        # Create a ticket
        Ticket.objects.create(
            name="Test Ticket 1",
            event=self.event,
            nummer="A1B2C3D4",
            author=self.user,
        )
        # Attempt to create another ticket with the same number
        self.payload["nummer"] = "A1B2C3D4"
        response = self.client.post(
            reverse("events:ticket_create"),
            self.payload,
        )

        self.assertEqual(response.status_code, 200)  # Form re-renders on error
        self.assertEqual(Ticket.objects.count(), 1)  # No new ticket created

    def test_unauthenticated_user(self):
        # Logout user and try to create a ticket
        self.client.logout()
        response = self.client.post(
            reverse("events:ticket_create"),
            self.payload,
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertEqual(Ticket.objects.count(), 0)
