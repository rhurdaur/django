""" 
URLs für die user-Api

nutzt authtoken-View um einen Token bereitzustellen
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("token", obtain_auth_token, name="user-token"),  # muss via POST
]
