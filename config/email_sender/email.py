from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.base import ContextMixin
from django.conf import settings

from email_sender.constants import Messages


class BaseSendEmail(ContextMixin):
    """
    Базовый класс для отправки сообщений на email
    """
    template_name_html = None
    subject = None

    def __init__(self, context=None,  template_name_html=None,  subject=None, *args, **kwargs):
        super(BaseSendEmail, self).__init__(*args, **kwargs)

        self.context = {} if context is None else context

        if template_name_html is not None:
            self.template_name_html = template_name_html

        if subject is not None:
            self.subject = subject

    def get_context_data(self, **kwargs):
        ctx = super(BaseSendEmail, self).get_context_data(**kwargs)
        context = dict(ctx, **self.context)
        domain = context.get('domain') or getattr(settings, 'DOMAIN', '')
        protocol = context.get('protocol') or 'http'
        site_name = context.get('site_name') or getattr(
            settings, 'SITE_NAME', ''
        )
        user = context.get('user')

        context.update({
            'domain': domain,
            'protocol': protocol,
            'site_name': site_name,
            'user': user
        })
        return context

    def get_html_message(self):
        context = self.get_context_data()
        return render_to_string(self.template_name_html, context)

    def send(self, to):
        html_message = self.get_html_message()
        plain_message = strip_tags(html_message)
        send_mail(self.subject, plain_message, settings.DEFAULT_FROM_EMAIL, to, html_message=html_message)


class VacancySendEmail(BaseSendEmail):
    """
    Отправляет оповещение об отклике на вакансию
    """
    template_name_html = "email_sender/email/vacancy.html"
    subject = Messages.EMAIL_SUBJECT_VACANCY


class QuestionnaireSendEmail(BaseSendEmail):
    """
    Отправляет оповещение об отклике на анкету
    """
    template_name_html = "email_sender/email/questionnaire.html"
    subject = Messages.EMAIL_SUBJECT_QUESTIONNAIRE


class ForgotPasswordSendEmail(BaseSendEmail):
    template_name_html = "email_sender/email/email_forgot_password.html"
    subject = Messages.EMAIL_FORGOT_PASSWORD


class SignUpSendEmail(BaseSendEmail):
    template_name_html = "email_sender/email/email_sign_up.html"
    subject = Messages.EMAIL_SIGN_UP
