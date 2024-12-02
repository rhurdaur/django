from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class User(AbstractUser):
    address = models.CharField(max_length=250, blank=True, null=True)
