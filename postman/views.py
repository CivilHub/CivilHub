from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
try:
    from django.contrib.sites.shortcuts import get_current_site  # Django 1.7
except ImportError:
    from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
try:
    from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit  # Django 1.4.11, 1.5.5
except ImportError:
    from urlparse import urlsplit, urlunsplit
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now
from django.utils.translation import ugettext as _, ugettext_lazy as lz_
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, TemplateView, View

from . import OPTION_MESSAGES
from .fields import autocompleter_app
from .forms import WriteForm, AnonymousWriteForm, QuickReplyForm, FullReplyForm
from .models import Message, get_order_by
from .utils import format_subject, format_body

login_required_m = method_decorator(login_required)
csrf_protect_m = method_decorator(csrf_protect)


##########
# Helpers
##########
def _get_referer(request):
    """Return the HTTP_REFERER, if existing."""
    if 'HTTP_REFERER' in request.META:
        sr = urlsplit(request.META['HTTP_REFERER'])
        return urlunsplit(('', '', sr.path, sr.query, sr.fragment))


########
# Views
########
class FolderMixin(object):
    """Code common to the folders."""
    http_method_names = ['get']

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(FolderMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FolderMixin, self).get_context_data(**kwargs)
        params = {}
        option = kwargs.get('option')
        if option:
            params['option'] = option
        order_by = get_order_by(self.request.GET)
        if order_by:
            params['order_by'] = order_by
        msgs = getattr(Message.objects, self.folder_name)(self.request.user, **params)
        context.update({
            'pm_messages': msgs,  # avoid 'messages', already used by contrib.messages
            'by_conversation': option is None,
            'by_message': option == OPTION_MESSAGES,
            'by_conversation_url': reverse(self.view_name),
            'by_message_url': reverse(self.view_name, args=[OPTION_MESSAGES]),
            'current_url': self.request.get_full_path(),
            'gets': self.request.GET,  # useful to postman_order_by template tag
        })
        return context


class InboxView(FolderMixin, TemplateView):
    """
    Display the list of received messages for the current user.

    Optional URLconf name-based argument:
        ``option``: display option:
            OPTION_MESSAGES to view all messages
            default to None to view only the last message for each conversation
    Optional URLconf configuration attribute:
        ``template_name``: the name of the template to use

    """
    # for FolderMixin:
    folder_name = 'inbox'
    view_name = 'postman_inbox'
    # for TemplateView:
    template_name = 'postman/inbox.html'


class SentView(FolderMixin, TemplateView):
    """
    Display the list of sent messages for the current user.

    Optional arguments and attributes: refer to InboxView.

    """
    # for FolderMixin:
    folder_name = 'sent'
    view_name = 'postman_sent'
    # for TemplateView:
    template_name = 'postman/sent.html'


class ArchivesView(FolderMixin, TemplateView):
    """
    Display the list of archived messages for the current user.

    Optional arguments and attributes: refer to InboxView.

    """
    # for FolderMixin:
    folder_name = 'archives'
    view_name = 'postman_archives'
    # for TemplateView:
    template_name = 'postman/archives.html'


class TrashView(FolderMixin, TemplateView):
    """
    Display the list of deleted messages for the current user.

    Optional arguments and attributes: refer to InboxView.

    """
    # for FolderMixin:
    folder_name = 'trash'
    view_name = 'postman_trash'
    # for TemplateView:
    template_name = 'postman/trash.html'


class ComposeMixin(object):
    """
    Code common to the write and reply views.

    Optional attributes:
        ``success_url``: where to redirect to after a successful POST
        ``user_filter``: a filter for recipients
        ``exchange_filter``: a filter for exchanges between a sender and a recipient
        ``max``: an upper limit for the recipients number
        ``auto_moderators``: a list of auto-moderation functions

    """
    http_method_names = ['get', 'post']
    success_url = None
    user_filter = None
    exchange_filter = None
    max = None
    auto_moderators = []

    def get_form_kwargs(self):
        kwargs = super(ComposeMixin, self).get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({
                'sender': self.request.user,
                'user_filter': self.user_filter,
                'exchange_filter': self.exchange_filter,
                'max': self.max,
                'site': get_current_site(self.request),
            })
        return kwargs

    def get_success_url(self):
        return self.request.GET.get('next') or self.success_url or _get_referer(self.request) or 'postman_inbox'

    def form_valid(self, form):
        params = {'auto_moderators': self.auto_moderators}
        if hasattr(self, 'parent'):  # only in the ReplyView case
            params['parent'] = self.parent
        is_successful = form.save(**params)
        if is_successful:
            messages.success(self.request, _("Message successfully sent."), fail_silently=True)
        else:
            messages.warning(self.request, _("Message rejected for at least one recipient."), fail_silently=True)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ComposeMixin, self).get_context_data(**kwargs)
        context.update({
            'autocompleter_app': autocompleter_app,
            'next_url': self.request.GET.get('next') or _get_referer(self.request),
        })
        return context


class WriteView(ComposeMixin, FormView):
    """
    Display a form to compose a message.

    Optional URLconf name-based argument:
        ``recipients``: a colon-separated list of usernames
    Optional attributes:
        ``form_classes``: a 2-tuple of form classes
        ``autocomplete_channels``: a channel name or a 2-tuple of names
        ``template_name``: the name of the template to use
        + those of ComposeMixin

    """
    form_classes = (WriteForm, AnonymousWriteForm)
    autocomplete_channels = None
    template_name = 'postman/write.html'

    @csrf_protect_m
    def dispatch(self, *args, **kwargs):
        if getattr(settings, 'POSTMAN_DISALLOW_ANONYMOUS', False):
            return login_required(super(WriteView, self).dispatch)(*args, **kwargs)
        return super(WriteView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        return self.form_classes[0] if self.request.user.is_authenticated() else self.form_classes[1]

    def get_initial(self):
        initial = super(WriteView, self).get_initial()
        if self.request.method == 'GET':
            initial.update(self.request.GET.items())  # allow optional initializations by query string
            recipients = self.kwargs.get('recipients')
            if recipients:
                # order_by() is not mandatory, but: a) it doesn't hurt; b) it eases the test suite
                # and anyway the original ordering cannot be respected.
                user_model = get_user_model()
                usernames = list(user_model.objects.values_list(user_model.USERNAME_FIELD, flat=True).filter(
                    is_active=True,
                    **{'{0}__in'.format(user_model.USERNAME_FIELD): [r.strip() for r in recipients.split(':') if r and not r.isspace()]}
                ).order_by(user_model.USERNAME_FIELD))
                if usernames:
                    initial['recipients'] = ', '.join(usernames)
        return initial

    def get_form_kwargs(self):
        kwargs = super(WriteView, self).get_form_kwargs()
        if isinstance(self.autocomplete_channels, tuple) and len(self.autocomplete_channels) == 2:
            channel = self.autocomplete_channels[self.request.user.is_anonymous()]
        else:
            channel = self.autocomplete_channels
        kwargs['channel'] = channel
        return kwargs


class ReplyView(ComposeMixin, FormView):
    """
    Display a form to compose a reply.

    Optional attributes:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``autocomplete_channel``: a channel name
        ``template_name``: the name of the template to use
        + those of ComposeMixin

    """
    form_class = FullReplyForm
    formatters = (format_subject, format_body)
    autocomplete_channel = None
    template_name = 'postman/reply.html'

    @csrf_protect_m
    @login_required_m
    def dispatch(self, request, message_id, *args, **kwargs):
        perms = Message.objects.perms(request.user)
        self.parent = get_object_or_404(Message, perms, pk=message_id)
        return super(ReplyView, self).dispatch(request,*args, **kwargs)

    def get_initial(self):
        self.initial = self.parent.quote(*self.formatters)  # will also be partially used in get_form_kwargs()
        if self.request.method == 'GET':
            self.initial.update(self.request.GET.items())  # allow overwriting of the defaults by query string
        return self.initial

    def get_form_kwargs(self):
        kwargs = super(ReplyView, self).get_form_kwargs()
        kwargs['channel'] = self.autocomplete_channel
        if self.request.method == 'POST':
            if 'subject' not in kwargs['data']:  # case of the quick reply form
                post = kwargs['data'].copy()  # self.request.POST is immutable
                post['subject'] = self.initial['subject']
                kwargs['data'] = post
            kwargs['recipient'] = self.parent.sender or self.parent.email
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ReplyView, self).get_context_data(**kwargs)
        context['recipient'] = self.parent.obfuscated_sender
        return context


class DisplayMixin(object):
    """
    Code common to the by-message and by-conversation views.

    Optional attributes:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``template_name``: the name of the template to use

    """
    http_method_names = ['get']
    form_class = QuickReplyForm
    formatters = (format_subject, format_body if getattr(settings, 'POSTMAN_QUICKREPLY_QUOTE_BODY', False) else None)
    template_name = 'postman/view.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(DisplayMixin, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        self.msgs = Message.objects.thread(user, self.filter)
        if not self.msgs:
            raise Http404
        Message.objects.set_read(user, self.filter)
        return super(DisplayMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DisplayMixin, self).get_context_data(**kwargs)
        user = self.request.user
        # are all messages archived ?
        for m in self.msgs:
            if not getattr(m, ('sender' if m.sender == user else 'recipient') + '_archived'):
                archived = False
                break
        else:
            archived = True
        # look for the most recent received message (and non-deleted to comply with the future perms() control), if any
        for m in reversed(self.msgs):
            if m.recipient == user and not m.recipient_deleted_at:
                received = m
                break
        else:
            received = None
        context.update({
            'pm_messages': self.msgs,
            'archived': archived,
            'reply_to_pk': received.pk if received else None,
            'form': self.form_class(initial=received.quote(*self.formatters)) if received else None,
            'next_url': self.request.GET.get('next') or reverse('postman_inbox'),
        })
        return context


class MessageView(DisplayMixin, TemplateView):
    """Display one specific message."""

    def get(self, request, message_id, *args, **kwargs):
        self.filter = Q(pk=message_id)
        return super(MessageView, self).get(request, *args, **kwargs)


class ConversationView(DisplayMixin, TemplateView):
    """Display a conversation."""

    def get(self, request, thread_id, *args, **kwargs):
        self.filter = Q(thread=thread_id)
        return super(ConversationView, self).get(request, *args, **kwargs)


class UpdateMessageMixin(object):
    """
    Code common to the archive/delete/undelete actions.

    Attributes:
        ``field_bit``: a part of the name of the field to update
        ``success_msg``: the displayed text in case of success
    Optional attributes:
        ``field_value``: the value to set in the field
        ``success_url``: where to redirect to after a successful POST

    """
    http_method_names = ['post']
    field_value = None
    success_url = None

    @csrf_protect_m
    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(UpdateMessageMixin, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        next_url = _get_referer(request) or 'postman_inbox'
        pks = request.POST.getlist('pks')
        tpks = request.POST.getlist('tpks')
        if pks or tpks:
            user = request.user
            filter = Q(pk__in=pks) | Q(thread__in=tpks)
            recipient_rows = Message.objects.as_recipient(user, filter).update(**{'recipient_{0}'.format(self.field_bit): self.field_value})
            sender_rows = Message.objects.as_sender(user, filter).update(**{'sender_{0}'.format(self.field_bit): self.field_value})
            if not (recipient_rows or sender_rows):
                raise Http404  # abnormal enough, like forged ids
            messages.success(request, self.success_msg, fail_silently=True)
            return redirect(request.GET.get('next') or self.success_url or next_url)
        else:
            messages.warning(request, _("Select at least one object."), fail_silently=True)
            return redirect(next_url)


class ArchiveView(UpdateMessageMixin, View):
    """Mark messages/conversations as archived."""
    field_bit = 'archived'
    success_msg = lz_("Messages or conversations successfully archived.")
    field_value = True


class DeleteView(UpdateMessageMixin, View):
    """Mark messages/conversations as deleted."""
    field_bit = 'deleted_at'
    success_msg = lz_("Messages or conversations successfully deleted.")
    field_value = now()


class UndeleteView(UpdateMessageMixin, View):
    """Revert messages/conversations from marked as deleted."""
    field_bit = 'deleted_at'
    success_msg = lz_("Messages or conversations successfully recovered.")
