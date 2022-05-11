# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime
from django.contrib.humanize.templatetags.humanize import naturaltime


class Dialog(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs",
                              on_delete=models.CASCADE)
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Личный диалог"
        verbose_name_plural = "Личные диалоги"
        unique_together = ['owner', 'opponent']
        
    def get_message_chat(self):
        msg = self.messages.filter().order_by('-id')
        if len(msg) > 0:
            msg = msg[0]
        return msg

    def get_sum_new_messages(self):
        a = self.messages.filter(read=False).exclude(sender=self.opponent).count()
        return a

    def get_sum_new_messages_owner(self):
        a = self.messages.filter(read=False).exclude(sender=self.owner).count()
        return a

    def get_list_message(self):
        return self.messages.filter().order_by('created')

    def __str__(self):
        return '{owner} и {opponent}'.format(owner=self.owner, opponent=self.opponent)


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Диалог"), related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Автор"), related_name="messages",
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Сообщение"))
    read = models.BooleanField(verbose_name=_("Прочитано"), default=False)
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Сообщение личного диалога"
        verbose_name_plural = "Сообщения личных диалогов"

    def get_formatted_create_datetime(self):
        return self.created.strftime("%H:%M %d/%m/%y")

    def get_last_time(self):
        return _('{}').format(naturaltime(self.created))

    def __str__(self):
        return self.sender.username + "(" + self.get_formatted_create_datetime() + ")"
