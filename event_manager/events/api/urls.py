from django.urls import path
from .views import (
    CategoryListCreateAPIView,
    EventListCreateAPIView,
    ReviewListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    CreateReviewView,
)


urlpatterns = [
    path("review/<int:event_pk>/", CreateReviewView.as_view(), name="create-review"),
    path(
        "",
        EventListCreateAPIView.as_view(),
        name="event-list-create",
    ),
    path(
        "<int:pk>",
        EventRetrieveUpdateDestroyAPIView.as_view(),
        name="event-retriev-update-destroy",
    ),
    path(
        "categories", CategoryListCreateAPIView.as_view(), name="categories-list-create"
    ),
    path(
        "reviews", ReviewListCreateAPIView.as_view(), name="review-list-create"
    ),  # post / get
]
