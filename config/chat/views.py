from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from . import models
from . import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Max


@method_decorator(login_required, name='dispatch')
class DialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat/dialogs.html'
    model = models.Dialog

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user)).annotate(last_message=Max('messages__created')).order_by('-last_message')
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('username'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
            dialog = utils.get_dialogs_with_user(self.request.user, user)
            if len(dialog) == 0:
                dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
            else:
                dialog = dialog[0]
            context['active_dialog'] = dialog
        else:
            if len(self.object_list) > 0:
                context['active_dialog'] = self.object_list[0]
            else:
                context['active_dialog'] = False
        if context['active_dialog'] :
            if self.request.user == context['active_dialog'].owner:
                context['opponent_username'] = context['active_dialog'].opponent.username
                context['opponent_user'] = context['active_dialog'].opponent
            else:
                context['opponent_username'] = context['active_dialog'].owner.username
                context['opponent_user'] = context['active_dialog'].owner
        return context
