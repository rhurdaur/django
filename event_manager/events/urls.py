from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("space", views.space_data, name="space-data"),
    path("categories", views.categories, name="categories"),
    path("categories/create", views.category_create, name="category_create"),
    # as_view erzeugt EinstiegsFunktion
    path("", views.EventListView.as_view(), name="events"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("create", views.EventCreateView.as_view(), name="event_create"),
    path("search", views.SearchEventView.as_view(), name="search_events"),
    path("<int:pk>/update", views.EventUpdateView.as_view(), name="event_update"),
    path("<int:pk>/delete", views.EventDeleteView.as_view(), name="event_delete"),
    path(
        "categories/<int:pk>",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("tickets", views.TicketListView.as_view(), name="ticket_list"),
    path("tickets/create/", views.TicketCreateView.as_view(), name="ticket_create"),
    path(
        "review/create/<int:event_pk>",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
]
