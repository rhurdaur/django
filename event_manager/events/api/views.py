from rest_framework import views
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import (
    CategorySerializer,
    EventCreateSerializer,
    EventSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from events.models import Category, Event, Review
from .permissions import IsAdminOrReadOnly


class CreateReviewView(ListCreateAPIView):
    """Create View / List VIew for specific Event

    api/events/createlist/4
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ReviewCreateSerializer

    def get_queryset(self):
        # Filter reviews for the specific event
        event_id = self.kwargs.get("event_pk")
        event = get_object_or_404(Event, id=event_id)
        return Review.objects.filter(event=event)

    def create(self, request, *args, **kwargs):
        # Fetch the event by primary key (pk)
        event_id = self.kwargs.get("event_pk")
        event = get_object_or_404(Event, id=event_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the serializer with additional fields: event and author
        serializer.save(event=event, author=self.request.user)
        return Response(serializer.data, status=201)


class EventRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Anzeigen, Updaten und Löschen einer einer Resource
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "DESTROY"]:
            return EventCreateSerializer
        return EventSerializer


class ReviewListCreateAPIView(ListCreateAPIView):
    """
    Auflisten aller Resourcen und Anlegen einer Resource
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class EventListCreateAPIView(ListCreateAPIView):
    queryset = Event.objects.prefetch_related("reviews")
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["date", "name"]
    search_fields = ["sub_title", "=name"]

    """
    SUCHE:
    http://127.0.0.1:8000/api/v1/category/?format=json&search=Indio

    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    '$' Regex search.

    """

    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # den Author der serializerInstanz übergeben,
        # damit es zu keinem Integrity Fehler kommt
        author = self.request.user
        serializer.save(author=author)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        return EventSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
