"""
User-factory erzeugt zufällige User-Objekte und trägt sie in die DB.   
"""
import factory 
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",) # verhindert doppelten Eintrag
    
    username = factory.Iterator(["bob", "alice", "trudy", "mallory", "eve", "grumpy"])
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("abc"))