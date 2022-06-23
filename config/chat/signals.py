from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from chat.utils import get_dialog, add_msg

User = get_user_model()


@receiver(post_save, sender=User)
def send_pin_activation_account(sender, instance, created, **kwargs):
    """
    Отправляет пользователю приветственное сообщение с чата поддержки
    """
    if created:
        text = "Добро пожаловать в сервис VAHTOWEEK! " \
               "При возникновении вопросов по функционалу сервиса, " \
               "пишите нам в этот чат, и мы своевременно решим вашу проблему !"
        sender = User.objects.get(username="support")
        dialog = get_dialog(sender, instance)
        add_msg(dialog, sender, text)
