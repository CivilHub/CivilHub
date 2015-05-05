"""
URLconf for tests.py usage.

"""
from __future__ import unicode_literals

from django.conf import settings
try:
    from django.conf.urls import patterns, include, url  # django 1.4
except ImportError:
    from django.conf.urls.defaults import *  # "patterns, include, url" is enough for django 1.3, "*" for django 1.2
from django.forms import ValidationError
from django.views.generic.base import RedirectView

from . import OPTIONS
from .views import (InboxView, SentView, ArchivesView, TrashView,
        WriteView, ReplyView, MessageView, ConversationView,
        ArchiveView, DeleteView, UndeleteView)


# user_filter function set
def user_filter_reason(user):
    if user.get_username() == 'bar':
        return 'some reason'
    return None
def user_filter_no_reason(user):
    return ''
def user_filter_false(user):
    return False
def user_filter_exception(user):
    if user.get_username() == 'bar':
        raise ValidationError(['first good reason', "anyway, I don't like {0}".format(user.get_username())])
    return None

# exchange_filter function set
def exch_filter_reason(sender, recipient, recipients_list):
    if recipient.get_username() == 'bar':
        return 'some reason'
    return None
def exch_filter_no_reason(sender, recipient, recipients_list):
    return ''
def exch_filter_false(sender, recipient, recipients_list):
    return False
def exch_filter_exception(sender, recipient, recipients_list):
    if recipient.get_username() == 'bar':
        raise ValidationError(['first good reason', "anyway, I don't like {0}".format(recipient.get_username())])
    return None

# auto-moderation function set
def moderate_as_51(message):
    return 51
def moderate_as_48(message):
    return (48, "some reason")
moderate_as_48.default_reason = 'some default reason'

# quote formatters
def format_subject(subject):
    return "Re_ " + subject
def format_body(sender, body):
    return "{0} _ {1}".format(sender, body)

postman_patterns = patterns('',
    # Basic set
    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', InboxView.as_view(), name='postman_inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(), name='postman_sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(), name='postman_archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(), name='postman_trash'),
    url(r'^write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(), name='postman_write'),
    url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='postman_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='postman_view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(), name='postman_view_conversation'),
    url(r'^archive/$', ArchiveView.as_view(), name='postman_archive'),
    url(r'^delete/$', DeleteView.as_view(), name='postman_delete'),
    url(r'^undelete/$', UndeleteView.as_view(), name='postman_undelete'),
    (r'^$', RedirectView.as_view(url='inbox/', permanent=True)),

    # Customized set
    # 'success_url'
    url(r'^write_sent/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(success_url='postman_sent'), name='postman_write_with_success_url_to_sent'),
    url(r'^reply_sent/(?P<message_id>[\d]+)/$', ReplyView.as_view(success_url='postman_sent'), name='postman_reply_with_success_url_to_sent'),
    url(r'^archive_arch/$', ArchiveView.as_view(success_url='postman_archives'), name='postman_archive_with_success_url_to_archives'),
    url(r'^delete_arch/$', DeleteView.as_view(success_url='postman_archives'), name='postman_delete_with_success_url_to_archives'),
    url(r'^undelete_arch/$', UndeleteView.as_view(success_url='postman_archives'), name='postman_undelete_with_success_url_to_archives'),
    # 'max'
    url(r'^write_max/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(max=1), name='postman_write_with_max'),
    url(r'^reply_max/(?P<message_id>[\d]+)/$', ReplyView.as_view(max=1), name='postman_reply_with_max'),
    # 'user_filter' on write
    url(r'^write_user_filter_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_reason), name='postman_write_with_user_filter_reason'),
    url(r'^write_user_filter_no_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_no_reason), name='postman_write_with_user_filter_no_reason'),
    url(r'^write_user_filter_false/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_false), name='postman_write_with_user_filter_false'),
    url(r'^write_user_filter_exception/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(user_filter=user_filter_exception), name='postman_write_with_user_filter_exception'),
    # 'user_filter' on reply
    url(r'^reply_user_filter_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_reason), name='postman_reply_with_user_filter_reason'),
    url(r'^reply_user_filter_no_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_no_reason), name='postman_reply_with_user_filter_no_reason'),
    url(r'^reply_user_filter_false/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_false), name='postman_reply_with_user_filter_false'),
    url(r'^reply_user_filter_exception/(?P<message_id>[\d]+)/$', ReplyView.as_view(user_filter=user_filter_exception), name='postman_reply_with_user_filter_exception'),
    # 'exchange_filter' on write
    url(r'^write_exch_filter_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_reason), name='postman_write_with_exch_filter_reason'),
    url(r'^write_exch_filter_no_reason/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_no_reason), name='postman_write_with_exch_filter_no_reason'),
    url(r'^write_exch_filter_false/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_false), name='postman_write_with_exch_filter_false'),
    url(r'^write_exch_filter_exception/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(exchange_filter=exch_filter_exception), name='postman_write_with_exch_filter_exception'),
    # 'exchange_filter' on reply
    url(r'^reply_exch_filter_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_reason), name='postman_reply_with_exch_filter_reason'),
    url(r'^reply_exch_filter_no_reason/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_no_reason), name='postman_reply_with_exch_filter_no_reason'),
    url(r'^reply_exch_filter_false/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_false), name='postman_reply_with_exch_filter_false'),
    url(r'^reply_exch_filter_exception/(?P<message_id>[\d]+)/$', ReplyView.as_view(exchange_filter=exch_filter_exception), name='postman_reply_with_exch_filter_exception'),
    # 'auto_moderators'
    url(r'^write_moderate/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(auto_moderators=(moderate_as_51,moderate_as_48)), name='postman_write_moderate'),
    url(r'^reply_moderate/(?P<message_id>[\d]+)/$', ReplyView.as_view(auto_moderators=(moderate_as_51,moderate_as_48)), name='postman_reply_moderate'),
    # 'formatters'
    url(r'^reply_formatters/(?P<message_id>[\d]+)/$', ReplyView.as_view(formatters=(format_subject, format_body)), name='postman_reply_formatters'),
    url(r'^view_formatters/(?P<message_id>[\d]+)/$', MessageView.as_view(formatters=(format_subject, format_body)), name='postman_view_formatters'),
    # auto-complete
    url(r'^write_ac/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(autocomplete_channels=('postman_multiple_as1-1', None)), name='postman_write_auto_complete'),
    url(r'^reply_ac/(?P<message_id>[\d]+)/$', ReplyView.as_view(autocomplete_channel='postman_multiple_as1-1'), name='postman_reply_auto_complete'),
    # 'template_name'
    url(r'^inbox_template/(?:(?P<option>'+OPTIONS+')/)?$', InboxView.as_view(template_name='postman/fake.html'), name='postman_inbox_template'),
    url(r'^sent_template/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(template_name='postman/fake.html'), name='postman_sent_template'),
    url(r'^archives_template/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(template_name='postman/fake.html'), name='postman_archives_template'),
    url(r'^trash_template/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(template_name='postman/fake.html'), name='postman_trash_template'),
    url(r'^write_template/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(template_name='postman/fake.html'), name='postman_write_template'),
    url(r'^reply_template/(?P<message_id>[\d]+)/$', ReplyView.as_view(template_name='postman/fake.html'), name='postman_reply_template'),
    url(r'^view_template/(?P<message_id>[\d]+)/$', MessageView.as_view(template_name='postman/fake.html'), name='postman_view_template'),
    url(r'^view_template/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(template_name='postman/fake.html'), name='postman_view_conversation_template'),
)

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),  # because of the login_required decorator
    (r'^messages/', include(postman_patterns)),
)

# because of fields.py/AutoCompleteWidget/render()/reverse()
if 'ajax_select' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^ajax_select/', include('ajax_select.urls')),  # django-ajax-selects
    )

# optional
if 'notification' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^notification/', include('notification.urls')),  # django-notification
    )
