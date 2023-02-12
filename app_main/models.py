from typing import Any

from django.contrib.auth import get_user_model
from django.db import models  # noqa: F401

User = get_user_model()


class Student(models.Model):
    user: Any = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="+"
    )
    username: Any = models.TextField(
        blank=True,
        null=True,
    )
    name: Any = models.TextField(
        blank=True,
        null=True,
    )
    lastname: Any = models.TextField(
        blank=True,
        null=True,
    )
    email: Any = models.EmailField(
        blank=True,
        null=True,
    )
    date: Any = models.DateTimeField(
        blank=True,
        null=True,
    )
    marks: Any = models.JSONField(
        blank=True,
        null=True,
    )
