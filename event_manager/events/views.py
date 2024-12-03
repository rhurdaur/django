from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models
from .forms import EventForm



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
    
class CategoryDetailView(DetailView):
    """
    /events/categories/3
    """
    model = models.Category
    

class EventUpdateView(UpdateView):
    """ 
    POST /events/3/update
    """
    model = models.Event 
    form_class = EventForm

class EventCreateView(CreateView):
    """ 
    POST /events/create
    """
    model = models.Event 
    form_class = EventForm
    
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
