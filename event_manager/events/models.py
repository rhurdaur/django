from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from event_manager.mixins import DateTimeMixin

User = get_user_model()



class Category(DateTimeMixin):
    
    name = models.CharField(max_length=100, unique=True)
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(
        help_text=_("Beschreibung der Kategorie"),
        null=True, blank=True
    )
    
    class Meta:
        ordering = ["name"]
        verbose_name = _("Kategorie")
        verbose_name_plural = _("Kategorien")
        
    def __str__(self) -> str:
        return self.name


class Event(DateTimeMixin):
    # thin view, fat model
    
    class Group(models.IntegerChoices):
        BIG = 10, _("mittelgroße Gruppe")
        SMALL = 2, _("sehr kleine Gruppe")
        LARGE = 20, _("große Gruppe")
    
    name = models.CharField(max_length=100, unique=True)
    sub_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(
        help_text=_("Beschreibung des Events"),
        null=True, blank=True
    )
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE,
                                 related_name="events")
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField()
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, 
                               related_name="events")
    min_group = models.IntegerField(choices=Group.choices)
    
    
    def __str__(self) -> str:
        return self.name
    
