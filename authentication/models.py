# authentication/models.py
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

class CustomUser(AbstractUser):
    user_permissions = models.ManyToManyField(Permission, blank=True)
