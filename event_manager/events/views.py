from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # für Funktionen
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from . import models
from .forms import EventForm, CategoryForm, TicketForm


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


class EventListView(ListView):
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
