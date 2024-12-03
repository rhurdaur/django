from django import forms 
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = "__all__"
        exclude = ("author",)
        
        widgets = {
            "date": forms.DateTimeInput(
                format=("%Y-%m-%d %H:%M"),
                attrs={"type": "datetime-local"}
            )
        }