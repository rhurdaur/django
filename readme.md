# Event Project GFU Django Kurs

## Installation

    git clone https://github.com/rhurdaur/djangoproject
    cd djangoproject

    python -m venv env
    .\env\Scripts\activate

    (env) pip install pip-tools
    (env) cd event_manager
    (env) pip-sync .\requirements.txt .\requirements-dev.txt

    (env) python manage.py createsuperuser
    (env) python manage.py create_user
    (env) python manage.py create_events --events 20


## folgende Apps wurden entwickelt

- User-App für das User-Model und die User-API
- Event-App für die Event-Verwaltung
- Core-App für die Verwaltung von misc


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