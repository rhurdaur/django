from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required  # für Funktionen
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from event_manager.mixins import CacheMixin
from . import models
from .forms import EventForm, CategoryForm, TicketForm, ReviewForm
from .services import fetch_data, ServiceApiError
from django.core.cache import cache


# @vary_on_cookie
# @cache_page(10)  # 5 sek
def space_data(request):
    """Aufrufen einer entfernten API zur Darstellung der Planeten."""
    url = "https://api.le-systeme-solaire.net/rest/bodies/"
    output = []

    # prüfen, ob im Cache drin!
    cache_key = "data"
    data = cache.get(cache_key)

    if not data:
        data = fetch_data(url, timeout=5)
        cache.set(cache_key, data, timeout=60)

    try:
        for body in data.get("bodies"):
            if body.get("isPlanet"):
                name = body.get("englishName")
                output.append(name)

    except ServiceApiError:
        data = []

    return render(request, "events/space_data.html", {"data": output})


class UserIsAuthor(UserPassesTestMixin):
    """User muss diesen Test bestehen."""

    def test_func(self):
        return self.get_object().author == self.request.user


class UserIsAuthorOrModerator(UserPassesTestMixin):
    """User ist Besitzer des Events oder Mitglied der Moderatoren-Gruppe."""

    def test_func(self):
        return (
            self.get_object().author == self.request.user
            or self.request.user.groups.filter(name="Moderatoren").exists()
        )


class TicketListView(LoginRequiredMixin, ListView):
    model = models.Ticket
    context_object_name = "tickets"

    def get_queryset(self):
        return models.Ticket.objects.filter(author=self.request.user)


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = TicketForm
    success_url = reverse_lazy("events:ticket_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = models.Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.event = self.event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("events:event_detail", kwargs={"pk": self.object.event.pk})

    def get_initial(self):
        self.event = get_object_or_404(models.Event, pk=self.kwargs["event_pk"])


# @login_required
def category_create(request):
    """
    View zum Anlegen einer Kategorie
    """

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            messages.warning(request, "Hier gibt es bald ein Problem")
            category = form.save()
            return redirect("events:category_detail", category.pk)
    else:
        form = CategoryForm()

    return render(request, "events/category_form.html", {"form": form})


def categories(request):
    """
    Listet die Kategorien auf.
    /events/categories
    """
    categories = models.Category.objects.all()

    return render(
        request,
        "events/categories.html",  # template
        {"categories": categories},  # context
    )


class EventDeleteView(UserIsAuthorOrModerator, DeleteView):
    model = models.Event
    success_url = reverse_lazy("events:events")  # reverse geht nicht


class EventUpdateView(SuccessMessageMixin, UserIsAuthorOrModerator, UpdateView):
    """
    POST /events/3/update
    """

    model = models.Event
    form_class = EventForm
    success_message = "Event wurde erfolgreich upgedated"


class CategoryDetailView(DetailView):
    """
    /events/categories/3
    """

    model = models.Category


class EventCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    POST /events/create
    """

    model = models.Event
    form_class = EventForm
    success_message = "Event wurde erfolgreich eingetragen"

    def form_valid(self, form):
        # falls Form valide, setze Author auf den eingeloggten
        # User
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventDetailView(DetailView):
    """
    /events/3
    """

    model = models.Event


class SearchEventView(ListView):
    model = models.Event

    def get_queryset(self):
        qs = super().get_queryset()  # Event.objects.all()
        searchTerm = self.request.GET.get("q")
        queryset = qs.filter(name__icontains=searchTerm)
        return queryset


class EventListView(CacheMixin, ListView):
    """
    Listet Events auf.

    /events
    """

    # auf https://ccbv.co.uk nachgucken, was überschrieben werden kann
    model = models.Event

    # Join bzw. Vorladen der benötigten Objekte (Performance-Gewinn!)
    # queryset = models.Event.objects.select_related("category", "author")
    queryset = models.Event.objects.prefetch_related("category", "author")

    # def get_queryset(self):
    #     qs = super().get_queryset()  # Event.objects.all() => select * from event
    #     # qs = qs.filter(name__contains=self.request.GET.get("q"))
    #     get = self.request.GET
    #     # einen 404-Fehler auslösen, falls User nicht vorhanden
    #     if "author" in get:
    #         user = get_object_or_404(
    #             get_user_model(),
    #             username=get.get("author"))
    #         qs = qs.filter(author=user)
    #     return qs
