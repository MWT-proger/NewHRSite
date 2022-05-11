from django import template

from app_main.models import GeneralSettings, Image

register = template.Library()


@register.simple_tag()
def get_general_settings():
    return GeneralSettings.objects.get(url='general')


@register.simple_tag()
def get_images():
    return Image.objects.all()
