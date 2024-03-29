from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from .models import Dialog, Message
from django.db.models import Q, Prefetch, Sum, Case, When, IntegerField, Count
import logging
import sys


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


async def get_user_from_session(session_key):
    """
    Gets the user from current User model using the passed session_key
    :param session_key: django.contrib.sessions.models.Session - session_key
    :return: User instance or None if not found
    """
    session = Session.objects.get(session_key=session_key)
    if session:
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        user = get_user_model().objects.filter(id=uid).first()  # get object or none
        return user
    else:
        return None


def get_dialogs_with_user(user_1, user_2):
    """
    gets the dialog between user_1 and user_2
    :param user_1: the first user in dialog (owner or opponent)
    :param user_2: the second user in dialog (owner or opponent)
    :return: queryset which include dialog between user_1 and user_2 (queryset can be empty)
    """
    return Dialog.objects.select_related("owner", "opponent").prefetch_related("messages").filter(
        Q(owner=user_1, opponent=user_2) | Q(opponent=user_1, owner=user_2))


def get_dialogs_with_user_first(user_1, user_2):
    return Dialog.objects \
        .select_related("owner", "opponent") \
        .prefetch_related(Prefetch('messages',
                                   queryset=Message.objects
                                   .select_related("sender")
                                   .filter())) \
        .filter(Q(owner=user_1, opponent=user_2) | Q(opponent=user_1, owner=user_2)) \
        .annotate(num_messages=Count('messages')) \
        .first()


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt='%d.%m.%y %H:%M:%S')
logger = logging.getLogger('django-private-dialog')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
