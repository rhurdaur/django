from django.urls import path
from .views import SimpleView

urlpatterns = [
    path("simple", SimpleView.as_view(), name="simple"),
]
