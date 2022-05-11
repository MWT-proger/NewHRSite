from django.contrib import admin
from .models import Dialog, Message

admin.site.register(Dialog)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender", "dialog", "created", "read"
    )
    date_hierarchy = "created"
