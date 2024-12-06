from event_manager.settings.base import *


INSTALLED_APPS.extend(
    [
        "debug_toolbar",
        "django_extensions",
    ]
)
MIDDLEWARE.extend(
    [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
)

INTERNAL_IPS = [
    "127.0.0.1",
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
