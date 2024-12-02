from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ["id", "username", "address", "hallo"] # Übersicht
    list_display_links = ["id", "username"]  # anklickbar in Übersicht
    fieldsets = UserAdmin.fieldsets + (("Additional Infos", {"fields": ("address",)}),)
    
    def hallo(self, obj: User):
        # wird für jeden Datensatz von User aufgerufen
        return obj.date_joined


