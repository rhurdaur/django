from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models

# Aufgabe: get_queryset überschreiben
# 127.0.0.1:8000/events?author=bob


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


class EventListView(ListView):
    """
    Listet Events auf.

    /events
    """
    # auf https://ccbv.co.uk nachgucken, was überschrieben werden kann
    model = models.Event
    # queryset = models.Event.objects.filter(name__contains="ab")
    
    def get_queryset(self):
        qs = super().get_queryset()  # Event.objects.all()
        # qs = qs.filter(name__contains=self.request.GET.get("q"))
        get = self.request.GET
        # einen 404-Fehler auslösen, falls User nicht vorhanden
        if "author" in get:
            user = get_object_or_404(
                get_user_model(), 
                username=get.get("author"))
            qs = qs.filter(author=user)
        return qs
