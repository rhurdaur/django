""" 
Review - Implementierung

Es soll eine Review-Möglichkeit implmentiert werden, 
dazu gibt es ein Review-Model, Views(CreateView, DetailView)

Review-Model
--------------
- name 
- event (FK)
- user (FK)
- review_text (str, muss mind. 10 Zeichen haben)
- rating (1 - 6)


Mermaid 

erDiagram
    Review {
        int id PK
        string name
        int stars
        string review_text
        int event_id FK
        int user_id FK
    }
    Event {
        int id PK
        string name
    }
    User {
        int id PK
        string username
        string email
    }

    Review }o--|| Event : "belongs to"
    Review }o--|| User : "belongs to"


"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from events.factories import CategoryFactory, EventFactory, ReviewFactory
from user.factories import UserFactory
from events.models import Review, Event

User = get_user_model()


class ReviewFactoryTest(TestCase):
    def setUp(self):
        self.review = ReviewFactory()

    def test_factory_creates_review_object(self):
        self.assertIsInstance(self.review, Review)
        self.assertIsNotNone(self.review.id)  # wurde in DB gespeichert
        self.assertTrue(1 <= self.review.rating <= 6)

        self.assertIsInstance(self.review.event, Event)
        self.assertIsInstance(self.review.author, User)

    def test_factory_author_via_argument(self):
        """Testen, ob eine Fabrik, die per Argumentübergabe erstellt wurde,
        diese Objekte auch benutzt."""
        user = UserFactory()
        event = EventFactory()
        review = ReviewFactory(author=user, event=event)

        self.assertEqual(user.username, review.author.username)
        self.assertEqual(event.name, review.event.name)


class ReviewModelTest(TestCase):
    """Testen des Review Models."""

    def setUp(self):
        self.event = EventFactory()
        self.author = UserFactory()

    def test_review_model_creation(self):
        instance = Review.objects.create(
            author=self.author,
            event=self.event,
            review_text="Super Event Text!",
            rating=3,
            name="Event Name",
        )
        self.assertEqual(instance.name, "Event Name")
        self.assertEqual(instance.rating, 3)
