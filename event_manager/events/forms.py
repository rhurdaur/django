from django import forms 
from .models import Event, Category


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
                format=("%Y-%m-%d %H:%M"),
                attrs={"type": "datetime-local"}
            )
        }