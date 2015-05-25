from __future__ import unicode_literals

from django import forms
from django.contrib import admin
try:
    from django.contrib.sites.shortcuts import get_current_site  # Django 1.7
except ImportError:
    from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext, ugettext_lazy as _

from postman.models import Message, PendingMessage


class MessageAdminForm(forms.ModelForm):
    # class Meta:
        # model = Message
        # Django 1.6: "... must also define the Meta.fields attribute (or the Meta.exclude attribute) ..."
        # any version: "..., the easiest solution is to omit the Meta.model attribute, ..."
    class Media:
        css = { "all": ("postman/css/admin.css",) }

    def clean(self):
        """Check data validity and coherence."""
        cleaned_data = super(MessageAdminForm, self).clean()
        sender = cleaned_data.get('sender')
        recipient = cleaned_data.get('recipient')
        email = cleaned_data.get('email')
        errors = []
        if not sender and not recipient:
            errors.append(ugettext("Sender and Recipient cannot be both undefined."))
            if 'sender' in cleaned_data:
                del cleaned_data['sender']
            if 'recipient' in cleaned_data:
                del cleaned_data['recipient']
        elif sender and recipient:
            if email:
                errors.append(ugettext("Visitor's email is in excess."))
                if 'email' in cleaned_data:
                    del cleaned_data['email']
        else:
            if not email:
                errors.append(ugettext("Visitor's email is missing."))
                if 'email' in cleaned_data:
                    del cleaned_data['email']
        sent_at = cleaned_data.get('sent_at')
        read_at = cleaned_data.get('read_at')
        if read_at and read_at < sent_at:
            errors.append(ugettext("Reading date must be later to sending date."))
            if 'read_at' in cleaned_data:
                del cleaned_data['read_at']
        sender_deleted_at = cleaned_data.get('sender_deleted_at')
        if sender_deleted_at and sender_deleted_at < sent_at:
            errors.append(ugettext("Deletion date by sender must be later to sending date."))
            if 'sender_deleted_at' in cleaned_data:
                del cleaned_data['sender_deleted_at']
        recipient_deleted_at = cleaned_data.get('recipient_deleted_at')
        if recipient_deleted_at and recipient_deleted_at < sent_at:
            errors.append(ugettext("Deletion date by recipient must be later to sending date."))
            if 'recipient_deleted_at' in cleaned_data:
                del cleaned_data['recipient_deleted_at']
        replied_at = cleaned_data.get('replied_at')
        obj = self.instance
        if replied_at:
            len_begin = len(errors)
            if replied_at < sent_at:
                errors.append(ugettext("Response date must be later to sending date."))
            if not read_at:
                errors.append(ugettext("The message cannot be replied without having been read."))
            elif replied_at < read_at:
                errors.append(ugettext("Response date must be later to reading date."))
            if not obj.get_replies_count():
                errors.append(ugettext("Response date cannot be set without at least one reply."))
            if not obj.thread_id:
                errors.append(ugettext("The message cannot be replied without being in a conversation."))
            if len(errors) > len_begin:
                if 'replied_at' in cleaned_data:
                    del cleaned_data['replied_at']
        # if obj.parent_id and not obj.thread_id:# can't be set by the form
        if errors:
            raise forms.ValidationError(errors)

        self.initial_status = obj.moderation_status
        return cleaned_data


class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
    search_fields = ('subject', 'body')
    date_hierarchy = 'sent_at'
    list_display = ('subject', 'admin_sender', 'admin_recipient', 'sent_at', 'moderation_status')
    list_filter = ('moderation_status', )
    fieldsets = (
        (None, {'fields': (
            ('sender', 'recipient', 'email'),
            'sent_at',
            )}),
        (_('Message'), {'fields': (
            'subject',
            'body',
            ('parent', 'thread'),
            )}),
        (_('Dates'), {'classes': ('collapse', ), 'fields': (
            ('read_at', 'replied_at'),
            ('sender_archived', 'recipient_archived'),
            ('sender_deleted_at', 'recipient_deleted_at'),
            )}),
        (_('Moderation'), {'fields': (
            ('moderation_status', 'moderation_date', 'moderation_by'),
            'moderation_reason',
            )}),
    )
    readonly_fields = (
        'parent', 'thread',  # no reason to change, and anyway too many objects
        'moderation_date', 'moderation_by',  # automatically set at status change
    )
    radio_fields = {'moderation_status': admin.VERTICAL}

    def queryset(self, request):  # for Django <= 1.5
        return super(MessageAdmin, self).queryset(request).select_related('sender', 'recipient')

    def get_queryset(self, request):  # changed in Django 1.6: "The get_queryset method was previously named queryset."
        """
        Add a custom select_related() to avoid a bunch of queries for users
        in the 'change list' admin view.

        Setting 'list_select_related = True' is not efficient as the default
        select_related() does not follow foreign keys that have null=True.

        """
        return super(MessageAdmin, self).get_queryset(request).select_related('sender', 'recipient')

    # no need for transaction decorator, it's already managed by the Admin
    def save_model(self, request, obj, form, change):
        """
        Add some actions around the save.

        Before the save, adjust some constrained fields.
        After the save, update related objects and notify parties if needed.

        """
        obj.clean_moderation(form.initial_status, request.user)
        obj.clean_for_visitor()
        super(MessageAdmin, self).save_model(request, obj, form, change)
        obj.update_parent(form.initial_status)
        obj.notify_users(form.initial_status, get_current_site(request), is_auto_moderated=False)


class PendingMessageAdminForm(forms.ModelForm):
    # class Meta:  # see MessageAdminForm comments
        # model = PendingMessage
    class Media:
        css = { "all": ("postman/css/admin.css",) }

    def clean(self):
        """Set status according to the button used to submit."""
        cleaned_data = super(PendingMessageAdminForm, self).clean()
        obj = self.instance
        self.initial_status = obj.moderation_status
        # look for for button names provided by custom admin/postman/pendingmessage/change_form.html
        if '_saveasaccepted' in self.data:
            obj.set_accepted()
        elif '_saveasrejected' in self.data:
            obj.set_rejected()
        return cleaned_data


class PendingMessageAdmin(MessageAdmin):
    form = PendingMessageAdminForm
    search_fields = ()
    date_hierarchy = None
    actions = None
    list_display = ('subject', 'admin_sender', 'admin_recipient', 'sent_at')
    list_filter = ()
    fieldsets = (
        (None, {'fields': (
            'admin_sender', 'admin_recipient', 'sent_at',
            )}),
        (_('Message'), {'fields': (
            'subject',
            'body',
            )}),
        (_('Moderation'), {'fields': (
            'moderation_reason',
            )}),
    )
    readonly_fields = ('admin_sender', 'admin_recipient')

    def has_add_permission(self, request):
        "Adding is impossible"
        return False

    def has_delete_permission(self, request, obj=None):
        "Deleting is impossible"
        return False

admin.site.register(Message, MessageAdmin)
admin.site.register(PendingMessage, PendingMessageAdmin)
