from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
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
]
