from django.test import TestCase, Client
from django.urls import reverse
from events.factories import CategoryFactory, EventFactory

URL_CATEGORY_OVERVIEW = reverse("events:categories")

# Testklasse bauen
# Testmetode test_event_update_not_public
# Welcher Statuscode?
# assertRedirects(response, redirect_url) nutzen


class EventUrls(TestCase):
    def setUp(self):
        self.event = EventFactory()

    def test_event_update_not_public(self):
        """Prüfen, ob Weiterleitung auf login stattfindet."""
        self.client = Client()
        response = self.client.get(
            reverse("events:event_update", args=(self.event.pk,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/events/{self.event.pk}/update",
            target_status_code=200,
        )


class CategoryUrls(TestCase):
    def setUp(self):
        """wird vor jedem Test ausgeführt."""
        self.category = CategoryFactory()

    def test_categories_overview_public(self):
        """
        Vorbedingungen definieren:
        - mind. eine Kategorie muss existieren

        Nachbedigungen:
        -

        Schritte:
        - Client anlegen
        - Url aufrufen
        -

        Ergebnis:
        - Statuscode 200
        - Kategoriename muss im HTML-Quelltext zu finden sein
        - Template für Kategorie-Übersicht genutzt worden sein
        """
        self.client = Client()  # User-Agent
        response = self.client.get(URL_CATEGORY_OVERVIEW)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.category.name)
        self.assertTemplateUsed(response, template_name="events/categories.html")

    def test_category_details_public(self):
        "Prüft, ob eine Kategorie-Detailseite öffntlich erreichbar ist."
        self.client = Client()
        response = self.client.get(
            reverse("events:category_detail", args=(self.category.pk,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.category.name)
        self.assertTemplateUsed(response, template_name="events/category_detail.html")
