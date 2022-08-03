from django import template
from app_profile.models import Vacancy
from django.db.models import Count

register = template.Library()


@register.simple_tag()
def get_demo_vacancy():
    list_vacancy = (Vacancy.objects
                        .select_related("region", "profession")
                        .all()
                        .annotate(count_sentence_annotate=Count('count_sentence'))
                        .annotate(count_see_annotate=Count('count_see'))
    [:10])
    return list_vacancy
