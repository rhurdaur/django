# Event Project GFU Django Kurs

## Installation

    git clone https://github.com/rhurdaur/djangoproject
    cd djangoproject

    python -m venv env
    .\env\Scripts\activate

    (env) pip install pip-tools
    (env) cd event_manager
    (env) mv env_example .env
    (env) pip-sync .\requirements.txt .\requirements-dev.txt

    (env) python manage.py createsuperuser
    (env) python manage.py create_user
    (env) python manage.py create_events --events 20

## Hinweise
Die .env-Datei muss mit gültigen Werten gefüllt werden.

## folgende Apps wurden entwickelt

- User-App für das User-Model und die User-API
- Event-App für die Event-Verwaltung
- Core-App für die Verwaltung von misc

## Curl-Requests für die API

### Token holen
- curl -X POST -d "username=admin&password=abcd1234" http://127.0.0.1:8000/api/users/token

### ListCreateAPIView
- curl http://127.0.0.1:8000/api/events/ -H "Authorization: Token 4de1cf9d04dc8eb9d33b646cd5baeb7a17af8c19"


4de1cf9d04dc8eb9d33b646cd5baeb7a17af8c19

## Literatur
- [Docker angucken](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
- [Pip Tools](https://pip-tools.readthedocs.io/en/stable/)


## pip-tools

    pip-compile requirements.in
    pip-sync .\requirements.txt

Alternative zu pip-tools: uv, poetry, pipenv

## Django-Docs

### Tag 1

https://docs.djangoproject.com/en/5.1/ref/models/querysets/
https://docs.python.org/3/library/argparse.html
https://ccbv.co.uk


### Tag 2

https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

#### Crispy forms
https://djangoheroes.friendlybytes.net/working_with_forms/working_with_forms.html#crispy-forms

https://django-filter.readthedocs.io

[Elasticsearch](https://www.elastic.co/de/elasticsearch)

Postgres Fulltext-Search
https://docs.djangoproject.com/en/5.1/ref/contrib/postgres/search/

### Tag 3

https://djangoheroes.friendlybytes.net/extended_technics/message_framework.html#message-level

### Tag 4
https://djangoheroes.spielprinzip.com/organisation/organize_settings.html#django-environ
https://djangoheroes.spielprinzip.com/profiwissen/whitenoise.html#index-0
https://django-extensions.readthedocs.io/en/latest/
https://www.django-rest-framework.org/

### Tag 5
https://swagger.io/tools/swagger-ui/
https://www.django-rest-framework.org/
https://djangoheroes.friendlybytes.net/webapi/restful_api.html#openapi-spezifikation
https://drf-spectacular.readthedocs.io/en/latest/

### Django Filters einbinden in DRF
https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html

### Alternativie zu drf-spectacular
https://github.com/axnsan12/drf-yasg/

### Redis (performante Caching-Lösung)
https://de.wikipedia.org/wiki/Redis
https://github.com/jazzband/django-redis