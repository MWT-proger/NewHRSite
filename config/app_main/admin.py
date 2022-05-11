from django.contrib import admin
from django.contrib.auth import get_user_model

from app_main.models import GeneralSettings, Image

User = get_user_model()


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
