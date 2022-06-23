from django.contrib import admin
from .models import Dialog, Message, Distribution
from app_account.models import User
from django.db.models import Q

admin.site.register(Dialog)


def get_dialog(user, other_user):
    dialog = Dialog.objects.filter(
        Q(owner=user, opponent=other_user) | Q(opponent=user, owner=other_user))
    if dialog.exists():
        return dialog[0]
    else:
        return Dialog.objects.create(opponent=user, owner=other_user)


def add_msg(dialog, sender_user, message):
    msg = Message.objects.create(
        dialog=dialog,
        sender=sender_user,
        text=message
    )
    return msg


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
