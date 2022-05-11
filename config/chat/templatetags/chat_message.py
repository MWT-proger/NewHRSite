from django import template
from chat.models import Message
from django.db.models import Q

register = template.Library()


@register.simple_tag(takes_context=True)
def get_unread_msg(context):
    request = context['request']
    return Message.objects.filter(Q(dialog__owner=request.user) | Q(dialog__opponent=request.user), read=False).exclude(sender=request.user)
