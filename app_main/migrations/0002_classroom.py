# Generated by Django 4.1.7 on 2023-02-16 18:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app_main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClassRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(blank=True, null=True)),
                (
                    "lessons",
                    models.JSONField(blank=True, null=True, default=[]),
                ),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "student",
                    models.ManyToManyField(
                        blank=True, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
