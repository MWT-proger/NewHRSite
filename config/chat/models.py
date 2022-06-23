# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime
from django.contrib.humanize.templatetags.humanize import naturaltime

from app_account.models import User


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


GROUP_USERS = [
    ('all', 'Всем'),
    ('applicant', 'Соискателям'),
    ('employer', 'Работодателям'),
    ('choice', 'Выбранным пользователям'),

]
STATUS = [
    ('create', 'Создано'),
    ('ok', 'Успешно отправлено'),
    ('fail', 'Частично отправлено'),
    ('error', 'Не отправлено'),
]


class Distribution(models.Model):
    """Рассылка"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Отправитель"),
                               related_name="distribution_sender",
                               on_delete=models.PROTECT)
    status = models.CharField(verbose_name=_("Статус"), max_length=20, default='create', choices=STATUS)
    group_recipient = models.CharField('Кому отправить', max_length=20, default='all', choices=GROUP_USERS)

    choice_recipients = models.ManyToManyField(User, verbose_name="Выбор пользователей", blank=True,
                                               related_name="distribution_recipient",
                                               help_text='Выбор при необходимости')

    text = models.TextField(_("Сообщение"), null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("Рассылка")
        verbose_name_plural = _("Рассылки")
