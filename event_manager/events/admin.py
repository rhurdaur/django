from django.contrib import admin
from .models import Event, Category, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author", "name", "event", "rating"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    @admin.display(description="Events aktiv setzen")
    def set_active(self, request, queryset):
        queryset.update(is_active=True)

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)

    # Liste von Feldern in der Übersicht
    list_display = ["name", "author", "category", "is_active"]
    actions = ["set_active", "set_inactive"]
    search_fields = ["name"]  # Suchbox, die in Feld "name" sucht

    # Organisation von Felder auf der Detailseite
    fieldsets = (
        ("Standard info", {"fields": ("name", "author", "date", "category")}),
        (
            "Detail Infos",
            {"fields": ("description", "min_group", "sub_title", "is_active")},
        ),
    )
