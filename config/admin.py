from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Settings


@admin.register(Settings)
class SettingsAdmin(SingletonModelAdmin):
    ...
