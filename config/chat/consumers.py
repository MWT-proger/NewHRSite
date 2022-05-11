# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from app_account.models import User
from .models import Dialog, Message
from app_profile.models import Vacancy, Questionnaire
from django.db.models import Q


@database_sync_to_async
def get_user(username):
    user = User.objects.filter(username=username)
    if user.exists():
        return user[0]


@database_sync_to_async
def add_questionnaire_sentence(id, user):
    Questionnaire.objects.get(id=id).count_sentence.add(user)


@database_sync_to_async
def add_vacancy_sentence(id, user):
    Vacancy.objects.get(id=id).count_sentence.add(user)


@database_sync_to_async
def get_dialog(user, other_user):
    dialog = Dialog.objects.filter(
        Q(owner=user, opponent=other_user) | Q(opponent=user, owner=other_user))
    if dialog.exists():
        return dialog[0]
    else:
        return Dialog.objects.create(opponent=user, owner=other_user)


@database_sync_to_async
def read_msg(dialog, sender_user, msg_id):
    not_read = Message.objects.filter(dialog=dialog, read=False, pk=msg_id).exclude(sender=sender_user)
    if len(not_read) > 0:
        not_read[0].read = True
        not_read[0].save()
        return not_read[0]


@database_sync_to_async
def add_msg(dialog, sender_user, message):

    msg = Message.objects.create(
        dialog=dialog,
        sender=sender_user,
        text=message
    )
    return msg


class ChatConsumer(AsyncWebsocketConsumer):
    other_username = None
    my_group_name = None
    other_group_name = None
    user = None
    dialog = None
    msg = None

    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        other_user = await get_user(self.other_username)
        if self.user and other_user:
            self.dialog = await get_dialog(self.user, other_user)
            if self.dialog:
                self.other_group_name = 'chat_%s' % other_user.username
            self.my_group_name = 'chat_%s' % self.user.username

            # Join room group
            await self.channel_layer.group_add(
                self.my_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.my_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'new_message':

            if self.user and self.dialog:
                message = text_data_json['message']
                try:
                    if text_data_json['application'] == 'vacancy':
                        await add_questionnaire_sentence(text_data_json['application_id'], self.user)
                    if text_data_json['application'] == 'questionnaire':
                        await add_vacancy_sentence(text_data_json['application_id'], self.user)
                except KeyError:
                    pass
                self.msg = await add_msg(self.dialog, self.user, message)

                if self.msg:
                    # Send message to room group
                    await self.channel_layer.group_send(
                        self.my_group_name,
                        {
                            'type': 'new_message',
                            'dialog_id': self.dialog.id,
                            'message': message,
                            'msg_id': self.msg.id,
                            'created': str(self.msg.get_formatted_create_datetime()),
                            'sender_username': self.user.username

                        }
                    )

                    await self.channel_layer.group_send(
                        self.other_group_name,
                        {
                            'type': 'new_message',
                            'dialog_id': self.dialog.id,
                            'message': message,
                            'msg_id': self.msg.id,
                            'created': str(self.msg.get_formatted_create_datetime()),
                            'sender_username': self.user.username
                        }
                    )
        if text_data_json['type'] == 'read_message':
            if self.user and self.dialog:
                msg_id = text_data_json['msg_id']
                self.msg = await read_msg(self.dialog, self.user, msg_id)

                if self.msg:
                    await self.channel_layer.group_send(
                        self.other_group_name,
                        {
                            'type': 'read_message',
                            'dialog_id': self.dialog.id,
                            'msg_id': self.msg.id,
                            'username_reader': self.user.username
                        }
                    )

    # Receive message from room group
    async def new_message(self, event):
        message = event['message']
        created = event['created']
        sender_username = event['sender_username']
        msg_id = event['msg_id']
        type = event['type']
        dialog_id = event['dialog_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'dialog_id': dialog_id,
            'message': message,
            'msg_id': msg_id,
            'created': created,
            'sender_username': sender_username
        }))

    # Receive message from room group
    async def read_message(self, event):
        username_reader = event['username_reader']
        msg_id = event['msg_id']
        type = event['type']
        dialog_id = event['dialog_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': type,
            'dialog_id': dialog_id,
            'msg_id': msg_id,
            'username_reader': username_reader
        }))
