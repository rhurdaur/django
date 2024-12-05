from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include("events.api.urls")),
] + debug_toolbar_urls()
