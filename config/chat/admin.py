from django.contrib import admin

from .models import Dialog, Message, Distribution
from app_account.models import User
from chat.utils import get_dialog, add_msg

admin.site.register(Dialog)


def body_mass_mailing(recipients, query):
    for recipient in recipients:
        dialog = get_dialog(query.sender, recipient)
        add_msg(dialog, query.sender, query.text)
    query.status = 'ok'
    query.save()
    return query.status


@admin.action(
    description="Отправить заготовок",
)
def send_message(modeladmin, request, queryset):
    query = queryset[0]
    if query.status == "create":
        if query.group_recipient == "all":
            recipients = User.objects.all()
            body_mass_mailing(recipients, query)

        elif query.group_recipient == "applicant":
            recipients = User.objects.filter(type="applicant")
            body_mass_mailing(recipients, query)

        elif query.group_recipient == "employer":
            recipients = User.objects.filter(type="employer")
            body_mass_mailing(recipients, query)

        elif query.group_recipient == "choice":
            recipients = query.choice_recipients.all()
            body_mass_mailing(recipients, query)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender", "dialog", "created", "read"
    )
    date_hierarchy = "created"


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    actions = [
        send_message
    ]
