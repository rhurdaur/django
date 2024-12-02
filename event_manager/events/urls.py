from django.urls import path
from . import views

urlpatterns = [
    path("categories", views.categories, name="categories"),
    # as_view erzeugt EinstiegsFunktion
    path("", views.EventListView.as_view(),  name="events"),
]
