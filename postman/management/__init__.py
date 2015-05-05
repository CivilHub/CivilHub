from __future__ import unicode_literals
import sys

from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

name = getattr(settings, 'POSTMAN_NOTIFIER_APP', 'notification')
if name and name in settings.INSTALLED_APPS:
    name = name + '.models'
    __import__(name)
    notification = sys.modules[name]
    try:
        create = notification.NoticeType.create  # django-notification 1.0
    except AttributeError:
        create = notification.create_notice_type  # django-notification 0.2.0 (works only with DJ <= 1.3)

    def create_notice_types(*args, **kwargs):
        create("postman_rejection", _("Message Rejected"), _("Your message has been rejected"))
        create("postman_message", _("Message Received"), _("You have received a message"))
        create("postman_reply", _("Reply Received"), _("You have received a reply"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)

