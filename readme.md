# Event Project GFU Django Kurs

## Installation

    git clone https://github.com/rhurdaur/djangoproject
    python -m venv env
    .\env\Scripts\activate

    (env) pip install pip-tools
    (env) pip-sync .\requirements.txt .\requirements-dev.txt

    (env) python manage.py createsuperuser
    (env) python manage.py create_user
    (env) python manage.py create_events

## Literatur
- [Docker angucken](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
- [Pip Tools](https://pip-tools.readthedocs.io/en/stable/)


## pip-tools

    pip-compile requirements.in
    pip-sync .\requirements.txt

Alternative zu pip-tools: uv, poetry, pipenv

## Django-Docs

### Montag

https://docs.djangoproject.com/en/5.1/ref/models/querysets/