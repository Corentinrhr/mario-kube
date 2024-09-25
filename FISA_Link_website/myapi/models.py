# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission # type: ignore
from django.db import models # type: ignore

class CustomUser(AbstractUser):
    email_perso = models.EmailField(unique=True, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Utilisez un nom unique
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Utilisez un nom unique
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user'
    )

from django.contrib.auth.models import AbstractBaseUser # type: ignore

class User(AbstractBaseUser):
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)