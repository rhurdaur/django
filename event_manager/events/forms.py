from django import forms
from django.core.exceptions import ValidationError
from .models import Event, Category, Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ("author",)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ("author", "event")

        widgets = {
            "rating": forms.RadioSelect(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = "__all__"
        exclude = ("author",)

        widgets = {
            "date": forms.DateTimeInput(
                format=("%Y-%m-%d %H:%M"), attrs={"type": "datetime-local"}
            )
        }
        # Die Formularfeld-Labels anpassen
        labels = {
            "name": "Event Name",
            "description": "Beschreibung",
        }

    def clean_sub_title(self):
        """Prüfe Sub-Title mit illegalen Zeichen beginnen.

        Hinweis: die clean-Methoden haben das Schema clean_<FELDNAME>.
        Die Feldwerte werden aus dem cleaned_data-Dict geholt, bereinigt/geprüft
        und zurückgegeben
        """
        sub_title = self.cleaned_data["sub_title"]
        illegal_chars = ("*", "#", ":")

        if isinstance(sub_title, str) and sub_title.startswith(illegal_chars):
            raise ValidationError(
                "Dieses Zeichen ist nicht erlaubt am Anfang des Sub-Titles."
            )

        return sub_title

    def clean_description(self):
        description = self.cleaned_data["description"]
        if isinstance(description, str) and len(description) < 5:
            raise ValidationError("description should be longer than 5")

        return description
