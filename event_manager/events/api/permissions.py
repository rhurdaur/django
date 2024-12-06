""" 
Eigene Permissions für DRF-Views anlegen
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Ist der User ein Superuser? Ansonsten darf er nur lesen.
    """

    def has_permission(self, request, view) -> bool:
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )
