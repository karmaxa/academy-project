from django.contrib import admin  # noqa: F401

from app_main import models


@admin.register(models.Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ClassRoom)
class ClassRoomModelAdmin(admin.ModelAdmin):
    pass
