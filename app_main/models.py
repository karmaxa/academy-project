from typing import Any

from django import urls
from django.contrib.auth import get_user_model
from django.db import models  # noqa: F401
from django.template.defaultfilters import slugify

User = get_user_model()


class Profile(models.Model):
    user: Any = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
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
        default=dict,
    )
    role: Any = models.TextField(
        blank=True,
        null=True,
    )
    searchtxt: Any = models.TextField(
        blank=True,
        null=True,
    )
    searchrole: Any = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return " ".join([self.name, self.lastname])


class ClassRoom(models.Model):
    name: Any = models.TextField(
        blank=True,
        null=True,
    )
    teacher: Any = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    student: Any = models.ManyToManyField(
        User,
        blank=True,
    )
    lessons: Any = models.JSONField(
        blank=True,
        null=True,
        default=list,
    )
    slug: Any = models.SlugField(
        blank=True,
        null=True,
    )

    def __str__(self) -> Any:
        return self.name

    def get_absolute_url(self, *args: Any, **kwargs: Any) -> str:
        return urls.reverse("classroom", kwargs={"slug": self.slug})

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save()
