"""
Test suite.

- Do not put 'mailer' in INSTALLED_APPS, it disturbs the emails counting.
- Make sure these templates are accessible:
    registration/login.html
    base.html
    404.html

To have a fast test session, set a minimal configuration as:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ':memory:',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',  # is optional
    'django.contrib.admin',
    # 'pagination',  # has to be before postman ; or use the mock
    # 'ajax_select',  # is an option
    # 'notification',  # is an option
    'postman',
)

"""
from __future__ import unicode_literals
import copy
from datetime import datetime, timedelta
import re
import sys

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, clear_url_caches, get_resolver, get_urlconf
from django.db.models import Q
from django.http import QueryDict
from django.template import Template, Context, TemplateSyntaxError, TemplateDoesNotExist
from django.test import TestCase, TransactionTestCase
from django.utils.encoding import force_text
from django.utils.formats import localize
from django.utils import six
from django.utils.six.moves import reload_module
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    now = datetime.now
from django.utils.translation import activate, deactivate

from . import OPTION_MESSAGES
from .api import pm_broadcast, pm_write
# because of reload()'s, do "from postman.fields import CommaSeparatedUserField" just before needs
# because of reload()'s, do "from postman.forms import xxForm" just before needs
from .models import ORDER_BY_KEY, ORDER_BY_MAPPER, Message, PendingMessage,\
        STATUS_PENDING, STATUS_ACCEPTED, STATUS_REJECTED,\
        get_order_by, get_user_representation
# because of reload()'s, do "from postman.utils import notification" just before needs
from .utils import format_body, format_subject


class GenericTest(TestCase):
    """
    Usual generic tests.
    """
    def test_version(self):
        self.assertEqual(sys.modules['postman'].__version__, "3.2.2")


class TransactionViewTest(TransactionTestCase):
    """
    Test some transactional behavior.
    Can't use Django TestCase class, because it has a special treament for commit/rollback to speed up the database resetting.
    """
    urls = 'postman.urls_for_tests'

    def setUp(self):
        self.user1 = get_user_model().objects.create_user('foo', 'foo@domain.com', 'pass')
        self.user2 = get_user_model().objects.create_user('bar', 'bar@domain.com', 'pass')

    def test(self):
        "Test possible clash between transaction.commit_on_success and transaction.atomic (Django 1.6)."
        url = reverse('postman_write')
        data = {'recipients': self.user2.get_username(), 'subject': 's'}
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.post(url, data)
        self.assertTrue(Message.objects.get())


class BaseTest(TestCase):
    """
    Common configuration and helper functions for all tests.
    """
    urls = 'postman.urls_for_tests'

    def setUp(self):
        deactivate()  # necessary for 1.4 to consider a new settings.LANGUAGE_CODE; 1.3 is fine with or without
        settings.LANGUAGE_CODE = 'en'  # do not bother about translation ; needed for the server side
        # added for 1.8, for the client side, to supersede the default language set as soon as the creation of auth's permissions,
        # initiated via a post_migrate signal.
        activate('en')
        for a in (
            'POSTMAN_DISALLOW_ANONYMOUS',
            'POSTMAN_DISALLOW_MULTIRECIPIENTS',
            'POSTMAN_DISALLOW_COPIES_ON_REPLY',
            'POSTMAN_DISABLE_USER_EMAILING',
            'POSTMAN_AUTO_MODERATE_AS',
            'POSTMAN_NOTIFIER_APP',
            'POSTMAN_SHOW_USER_AS',
            'POSTMAN_QUICKREPLY_QUOTE_BODY',
        ):
            if hasattr(settings, a):
                delattr(settings, a)
        settings.POSTMAN_MAILER_APP = None
        settings.POSTMAN_AUTOCOMPLETER_APP = {
            'arg_default': 'postman_single_as1-1',  # no default, mandatory to enable the feature
        }
        self.reload_modules()

        self.user1 = get_user_model().objects.create_user('foo', 'foo@domain.com', 'pass')
        self.user2 = get_user_model().objects.create_user('bar', 'bar@domain.com', 'pass')
        self.user3 = get_user_model().objects.create_user('baz', 'baz@domain.com', 'pass')
        self.email = 'qux@domain.com'

    def check_now(self, dt):
        "Check that a date is now. Well... almost."
        delta = dt - now()
        seconds = delta.days * (24*60*60) + delta.seconds
        self.assertTrue(-2 <= seconds <= 1)  # -1 is not enough for Mysql

    def check_status(self, m, status=STATUS_PENDING, is_new=True, is_replied=False, parent=None, thread=None,
        moderation_date=False, moderation_by=None, moderation_reason='',
        sender_archived=False, recipient_archived=False,
        sender_deleted_at=False, recipient_deleted_at=False):
        "Check a bunch of properties of a message."

        self.assertEqual(m.is_pending(), status==STATUS_PENDING)
        self.assertEqual(m.is_rejected(), status==STATUS_REJECTED)
        self.assertEqual(m.is_accepted(), status==STATUS_ACCEPTED)
        self.assertEqual(m.is_new, is_new)
        self.assertEqual(m.is_replied, is_replied)
        self.check_now(m.sent_at)
        self.assertEqual(m.parent, parent)
        self.assertEqual(m.thread, thread)
        self.assertEqual(m.sender_archived, sender_archived)
        self.assertEqual(m.recipient_archived, recipient_archived)
        if sender_deleted_at:
            if isinstance(sender_deleted_at, datetime):
                self.assertEqual(m.sender_deleted_at, sender_deleted_at)
            else:
                self.assertNotEqual(m.sender_deleted_at, None)
        else:
            self.assertEqual(m.sender_deleted_at, None)
        if recipient_deleted_at:
            if isinstance(recipient_deleted_at, datetime):
                self.assertEqual(m.recipient_deleted_at, recipient_deleted_at)
            else:
                self.assertNotEqual(m.recipient_deleted_at, None)
        else:
            self.assertEqual(m.recipient_deleted_at, None)
        if moderation_date:
            if isinstance(moderation_date, datetime):
                self.assertEqual(m.moderation_date, moderation_date)
            else:
                self.assertNotEqual(m.moderation_date, None)
        else:
            self.assertEqual(m.moderation_date, None)
        self.assertEqual(m.moderation_by, moderation_by)
        self.assertEqual(m.moderation_reason, moderation_reason)

    def create(self, *args, **kwargs):
        "Create a message."
        kwargs.update(subject='s')
        return Message.objects.create(*args, **kwargs)

    def create_accepted(self, *args, **kwargs):
        "Create a message with a default status as 'accepted'."
        kwargs.setdefault('moderation_status', STATUS_ACCEPTED)
        return self.create(*args, **kwargs)

    # set of message creations
    def c12(self, *args, **kwargs):
        kwargs.update(sender=self.user1, recipient=self.user2)
        return self.create_accepted(*args, **kwargs)
    def c13(self, *args, **kwargs):
        kwargs.update(sender=self.user1, recipient=self.user3)
        return self.create_accepted(*args, **kwargs)
    def c21(self, *args, **kwargs):
        kwargs.update(sender=self.user2, recipient=self.user1)
        return self.create_accepted(*args, **kwargs)
    def c23(self, *args, **kwargs):
        kwargs.update(sender=self.user2, recipient=self.user3)
        return self.create_accepted(*args, **kwargs)
    def c32(self, *args, **kwargs):
        kwargs.update(sender=self.user3, recipient=self.user2)
        return self.create_accepted(*args, **kwargs)

    def reload_modules(self):
        "Reload some modules after a change in settings."
        clear_url_caches()
        try:
            reload_module(sys.modules['postman.utils'])
            reload_module(sys.modules['postman.fields'])
            reload_module(sys.modules['postman.forms'])
            reload_module(sys.modules['postman.views'])
            reload_module(sys.modules['postman.urls'])
        except KeyError:  # happens once at the setUp
            pass
        reload_module(get_resolver(get_urlconf()).urlconf_module)


class ViewTest(BaseTest):
    """
    Test the views.
    """
    def test_home(self):
        response = self.client.get('/messages/')
        self.assertRedirects(response, reverse('postman_inbox'), status_code=301, target_status_code=302)

    def check_folder(self, folder):
        url = reverse('postman_' + folder, args=[OPTION_MESSAGES])
        template = "postman/{0}.html".format(folder)
        # anonymous
        response = self.client.get(url)
        self.assertRedirects(response, "{0}?{1}={2}".format(settings.LOGIN_URL, REDIRECT_FIELD_NAME, url))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        url = reverse('postman_' + folder)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)

    def test_inbox(self):
        self.check_folder('inbox')

    def test_sent(self):
        self.check_folder('sent')

    def test_archives(self):
        self.check_folder('archives')

    def test_trash(self):
        self.check_folder('trash')

    def check_template(self, action, args):
        # don't want to bother with additional templates; test only the parameter passing
        url = reverse('postman_' + action + '_template', args=args)
        self.assertRaises(TemplateDoesNotExist, self.client.get, url)

    def test_template(self):
        "Test the 'template_name' parameter."
        m1 = self.c12()
        m1.read_at, m1.thread = now(), m1
        m2 = self.c21(parent=m1, thread=m1.thread)
        m1.replied_at = m2.sent_at; m1.save()
        self.assertTrue(self.client.login(username='foo', password='pass'))
        for actions, args in [
            (('inbox', 'sent', 'archives', 'trash', 'write'), []),
            (('view', 'view_conversation'), [m1.pk]),
            (('reply',), [m2.pk]),
        ]:
            for action in actions:
                self.check_template(action, args)

    def test_write_authentication(self):
        "Test permission and what template & form are used."
        url = reverse('postman_write')
        template = "postman/write.html"
        # anonymous is allowed
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        from postman.forms import AnonymousWriteForm
        self.assertTrue(isinstance(response.context['form'], AnonymousWriteForm))
        # anonymous is not allowed
        settings.POSTMAN_DISALLOW_ANONYMOUS = True
        self.reload_modules()
        response = self.client.get(url)
        self.assertRedirects(response, "{0}?{1}={2}".format(settings.LOGIN_URL, REDIRECT_FIELD_NAME, url))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        from postman.forms import WriteForm
        self.assertTrue(isinstance(response.context['form'], WriteForm))

    def test_write_recipient(self):
        "Test the passing of recipient names in URL."
        template = "postman/write.html"

        url = reverse('postman_write', args=['foo'])
        response = self.client.get(url)
        self.assertContains(response, 'value="foo"')

        url = reverse('postman_write', args=['foo:bar'])
        response = self.client.get(url)
        self.assertContains(response, 'value="bar, foo"')

        url = reverse('postman_write', args=[':foo::intruder:bar:a-b+c@d.com:foo:'])
        response = self.client.get(url)
        self.assertContains(response, 'value="bar, foo"')

        # because of Custom User Model, do allow almost any character, not only '^[\w.@+-]+$' of the legacy django.contrib.auth.User model
        get_user_model().objects.create_user("Le Créac'h", 'foobar@domain.com', 'pass')  # even: space, accentued, qootes
        url = reverse('postman_write', args=["Le Créac'h"])
        response = self.client.get(url)
        self.assertContains(response, 'value="Le Créac&#39;h"')

    def test_write_auto_complete(self):
        "Test the 'autocomplete_channels' parameter."
        url = reverse('postman_write_auto_complete')
        # anonymous
        response = self.client.get(url)
        f = response.context['form'].fields['recipients']
        if hasattr(f, 'channel'):  # app may not be in INSTALLED_APPS
            self.assertEqual(f.channel, 'postman_single_as1-1')
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        f = response.context['form'].fields['recipients']
        if hasattr(f, 'channel'):
            self.assertEqual(f.channel, 'postman_multiple_as1-1')

    def check_init_by_query_string(self, action, args=[]):
        template = "postman/{0}.html".format(action)
        url = reverse('postman_' + action, args=args)
        response = self.client.get(url + '?subject=that%20is%20the%20subject')
        self.assertContains(response, 'value="that is the subject"')
        response = self.client.get(url + '?body=this%20is%20my%20body')
        # before Dj 1.5: 'name="body">this is my body' ; after: 'name="body">\r\nthis is my body'
        self.assertContains(response, 'this is my body</textarea>')

    def test_write_querystring(self):
        "Test the prefilling by query string."
        self.check_init_by_query_string('write')

    def check_message(self, m, is_anonymous=False, subject='s', body='b', recipient_username='bar'):
        "Check some message properties, status, and that no mail is sent."
        self.assertEqual(m.subject, subject)
        self.assertEqual(m.body, body)
        self.assertEqual(m.email, 'a@b.com' if is_anonymous else '')
        self.assertEqual(m.sender, self.user1 if not is_anonymous else None)
        self.assertEqual(m.recipient.get_username(), recipient_username)
        if is_anonymous:
            self.check_status(m, sender_deleted_at=True)
        self.assertEqual(len(mail.outbox), 0)

    def check_contrib_messages(self, response, text):
        if 'messages' in response.context:  # contrib\messages\context_processors.py may be not there
            messages = response.context['messages']
            if messages != []:  # contrib\messages\middleware.py may be not there
                self.assertEqual(len(messages), 1)
                for message in messages:  # can only be iterated
                    self.assertEqual(str(message), text)

    def check_write_post(self, extra={}, is_anonymous=False):
        "Check message generation, redirection, and mandatory fields."
        url = reverse('postman_write')
        url_with_success_url = reverse('postman_write_with_success_url_to_sent')
        data = {'recipients': self.user2.get_username(), 'subject': 's', 'body': 'b'}
        data.update(extra)
        # default redirect is to the requestor page
        response = self.client.post(url, data, HTTP_REFERER=url, follow=True)
        self.assertRedirects(response, url)
        self.check_contrib_messages(response, 'Message successfully sent.')  # no such check for the following posts, one is enough
        m = Message.objects.get()
        pk = m.pk
        self.check_message(m, is_anonymous)
        # fallback redirect is to inbox. So redirect again when login is required
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('postman_inbox'), target_status_code=302 if is_anonymous else 200)
        self.check_message(Message.objects.get(pk=pk+1), is_anonymous)
        # redirect url may be superseded
        response = self.client.post(url_with_success_url, data, HTTP_REFERER=url)
        self.assertRedirects(response, reverse('postman_sent'), target_status_code=302 if is_anonymous else 200)
        self.check_message(Message.objects.get(pk=pk+2), is_anonymous)
        # query string has highest precedence
        response = self.client.post(url_with_success_url + '?next=' + url, data, HTTP_REFERER='does not matter')
        self.assertRedirects(response, url)
        self.check_message(Message.objects.get(pk=pk+3), is_anonymous)

        for f in data.keys():
            if f in ('body',): continue
            d = data.copy()
            del d[f]
            response = self.client.post(url, d, HTTP_REFERER=url)
            self.assertFormError(response, 'form', f, 'This field is required.')

    def test_write_post_anonymous(self):
        self.check_write_post({'email': 'a@b.com'}, is_anonymous=True)

    def test_write_post_authenticated(self):
        self.assertTrue(self.client.login(username='foo', password='pass'))
        self.check_write_post()

    def test_write_post_multirecipient(self):
        "Test number of recipients constraint."
        from postman.fields import CommaSeparatedUserField
        url = reverse('postman_write')
        data = {
            'email': 'a@b.com', 'subject': 's', 'body': 'b',
            'recipients': '{0}, {1}'.format(self.user2.get_username(), self.user3.get_username())}
        # anonymous
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', CommaSeparatedUserField.default_error_messages['max'].format(limit_value=1, show_value=2))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        del data['email']
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        msgs = list(Message.objects.all())
        self.check_message(msgs[0], recipient_username='baz')
        self.check_message(msgs[1])

        url_with_max = reverse('postman_write_with_max')
        response = self.client.post(url_with_max, data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', CommaSeparatedUserField.default_error_messages['max'].format(limit_value=1, show_value=2))

        settings.POSTMAN_DISALLOW_MULTIRECIPIENTS = True
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', CommaSeparatedUserField.default_error_messages['max'].format(limit_value=1, show_value=2))

    def test_write_post_filters(self):
        "Test user- and exchange- filters."
        url = reverse('postman_write')
        data = {
            'subject': 's', 'body': 'b',
            'recipients': '{0}, {1}'.format(self.user2.get_username(), self.user3.get_username())}
        self.assertTrue(self.client.login(username='foo', password='pass'))

        response = self.client.post(reverse('postman_write_with_user_filter_reason'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Some usernames are rejected: bar (some reason).")

        response = self.client.post(reverse('postman_write_with_user_filter_no_reason'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Some usernames are rejected: bar, baz.")

        response = self.client.post(reverse('postman_write_with_user_filter_false'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Some usernames are rejected: bar, baz.")

        response = self.client.post(reverse('postman_write_with_user_filter_exception'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', ['first good reason',"anyway, I don't like bar"])

        response = self.client.post(reverse('postman_write_with_exch_filter_reason'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Writing to some users is not possible: bar (some reason).")

        response = self.client.post(reverse('postman_write_with_exch_filter_no_reason'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Writing to some users is not possible: bar, baz.")

        response = self.client.post(reverse('postman_write_with_exch_filter_false'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Writing to some users is not possible: bar, baz.")

        response = self.client.post(reverse('postman_write_with_exch_filter_exception'), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', ['first good reason',"anyway, I don't like bar"])

    def test_write_post_moderate(self):
        "Test 'auto_moderators' parameter."
        url = reverse('postman_write')
        data = {'subject': 's', 'body': 'b', 'recipients': self.user2.get_username()}
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.post(reverse('postman_write_moderate'), data, HTTP_REFERER=url, follow=True)
        self.assertRedirects(response, url)
        self.check_contrib_messages(response, 'Message rejected for at least one recipient.')
        self.check_status(Message.objects.get(), status=STATUS_REJECTED, recipient_deleted_at=True,
            moderation_date=True, moderation_reason="some reason")

    def test_write_notification(self):
        "Test the fallback for the site name in the generation of a notification, when the django.contrib.sites app is not installed."
        settings.POSTMAN_AUTO_MODERATE_AS = True  # will generate an acceptance notification
        url = reverse('postman_write')
        data = {'subject': 's', 'body': 'b', 'recipients': self.user2.get_username()}
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        self.check_status(Message.objects.get(), status=STATUS_ACCEPTED, moderation_date=True)
        self.assertEqual(len(mail.outbox), 1)
        # can't use get_current_site(response.request) because response.request is not an HttpRequest and doesn't have a get_host attribute
        if Site._meta.installed:
            sitename = Site.objects.get_current().name
        else:
            sitename = "testserver"  # the SERVER_NAME environment variable is not accessible here
        self.assertTrue(sitename in mail.outbox[0].subject)

    def test_reply_authentication(self):
        "Test permission and what template & form are used."
        template = "postman/reply.html"
        pk = self.c21(body="this is my body").pk
        url = reverse('postman_reply', args=[pk])
        # anonymous
        response = self.client.get(url)
        self.assertRedirects(response, "{0}?{1}={2}".format(settings.LOGIN_URL, REDIRECT_FIELD_NAME, url))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        from postman.forms import FullReplyForm
        self.assertTrue(isinstance(response.context['form'], FullReplyForm))
        self.assertContains(response, 'value="Re: s"')
        self.assertContains(response, '\n\nbar wrote:\n&gt; this is my body\n</textarea>')
        self.assertEqual(response.context['recipient'], 'bar')

        settings.POSTMAN_QUICKREPLY_QUOTE_BODY = True  # no influence here, acts only for Quick Reply
        self.reload_modules()
        response = self.client.get(url)
        self.assertContains(response, 'value="Re: s"')
        self.assertContains(response, '\n\nbar wrote:\n&gt; this is my body\n</textarea>')

    def test_reply_formatters(self):
        "Test the 'formatters' parameter."
        template = "postman/reply.html"
        pk = self.c21(body="this is my body").pk
        url = reverse('postman_reply_formatters', args=[pk])
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        self.assertContains(response, 'value="Re_ s"')
        self.assertContains(response, 'bar _ this is my body</textarea>')  # POSTMAN_QUICKREPLY_QUOTE_BODY setting is not involved

    def test_reply_auto_complete(self):
        "Test the 'autocomplete_channel' parameter."
        pk = self.c21().pk
        url = reverse('postman_reply_auto_complete', args=[pk])
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        f = response.context['form'].fields['recipients']
        if hasattr(f, 'channel'):
            self.assertEqual(f.channel, 'postman_multiple_as1-1')

    def check_404(self, view_name, pk):
        "Return is a 404 page."
        url = reverse(view_name, args=[pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def check_reply_404(self, pk):
        self.check_404('postman_reply', pk)

    def test_reply_id(self):
        "Test all sort of failures."
        self.assertTrue(self.client.login(username='foo', password='pass'))
        # invalid message id
        self.check_reply_404(1000)
        # existent message but you are the sender, not the recipient
        self.check_reply_404(Message.objects.get(pk=self.c12().pk).pk) # create & verify really there
        # existent message but not yours at all
        self.check_reply_404(Message.objects.get(pk=self.c23().pk).pk)
        # existent message but not yet visible to you
        self.check_reply_404(Message.objects.get(pk=self.create(sender=self.user2, recipient=self.user1).pk).pk)
        # cannot reply to a deleted message
        self.check_reply_404(Message.objects.get(pk=self.c21(recipient_deleted_at=now()).pk).pk)

    def test_reply_querystring(self):
        "Test the prefilling by query string."
        self.assertTrue(self.client.login(username='foo', password='pass'))
        self.check_init_by_query_string('reply', [self.c21().pk])

    def test_reply_post(self):
        "Test message generation and redirection."
        pk = self.c21().pk
        url = reverse('postman_reply', args=[pk])
        url_with_success_url = reverse('postman_reply_with_success_url_to_sent', args=[pk])
        data = {'subject': 's', 'body': 'b'}
        self.assertTrue(self.client.login(username='foo', password='pass'))
        # default redirect is to the requestor page
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        # the check_contrib_messages() in test_write_post() is enough
        self.check_message(Message.objects.get(pk=pk+1))
        # fallback redirect is to inbox
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('postman_inbox'))
        self.check_message(Message.objects.get(pk=pk+2))
        # redirect url may be superseded
        response = self.client.post(url_with_success_url, data, HTTP_REFERER=url)
        self.assertRedirects(response, reverse('postman_sent'))
        self.check_message(Message.objects.get(pk=pk+3))
        # query string has highest precedence
        response = self.client.post(url_with_success_url + '?next=' + url, data, HTTP_REFERER='does not matter')
        self.assertRedirects(response, url)
        self.check_message(Message.objects.get(pk=pk+4))
        # missing subject is valid, as in quick reply
        response = self.client.post(url, {}, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        self.check_message(Message.objects.get(pk=pk+5), subject='Re: s', body='')

    def test_reply_post_copies(self):
        "Test number of recipients constraint."
        from postman.fields import CommaSeparatedUserField
        pk = self.c21().pk
        url = reverse('postman_reply', args=[pk])
        data = {'subject': 's', 'body': 'b', 'recipients': self.user3.get_username()}
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        self.check_message(Message.objects.get(pk=pk+1))
        self.check_message(Message.objects.get(pk=pk+2), recipient_username='baz')

        url_with_max = reverse('postman_reply_with_max', args=[pk])
        data.update(recipients='{0}, {1}'.format(self.user2.get_username(), self.user3.get_username()))
        response = self.client.post(url_with_max, data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', CommaSeparatedUserField.default_error_messages['max'].format(limit_value=1, show_value=2))

        settings.POSTMAN_DISALLOW_COPIES_ON_REPLY = True
        self.reload_modules()
        response = self.client.post(url, data, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        self.check_message(Message.objects.get(pk=pk+3))
        self.assertRaises(Message.DoesNotExist, Message.objects.get, pk=pk+4)

    def test_reply_post_filters(self):
        "Test user- and exchange- filters."
        pk = self.c21().pk
        url = reverse('postman_reply', args=[pk])
        data = {'subject': 's', 'body': 'b', 'recipients': '{0}, {1}'.format(self.user2.get_username(), self.user3.get_username())}
        self.assertTrue(self.client.login(username='foo', password='pass'))

        response = self.client.post(reverse('postman_reply_with_user_filter_reason', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Some usernames are rejected: bar (some reason).")

        response = self.client.post(reverse('postman_reply_with_user_filter_no_reason', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Some usernames are rejected: bar, baz.")

        response = self.client.post(reverse('postman_reply_with_user_filter_false', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Some usernames are rejected: bar, baz.")

        response = self.client.post(reverse('postman_reply_with_user_filter_exception', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', ['first good reason',"anyway, I don't like bar"])

        response = self.client.post(reverse('postman_reply_with_exch_filter_reason', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Writing to some users is not possible: bar (some reason).")

        response = self.client.post(reverse('postman_reply_with_exch_filter_no_reason', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Writing to some users is not possible: bar, baz.")

        response = self.client.post(reverse('postman_reply_with_exch_filter_false', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', "Writing to some users is not possible: bar, baz.")

        response = self.client.post(reverse('postman_reply_with_exch_filter_exception', args=[pk]), data, HTTP_REFERER=url)
        self.assertFormError(response, 'form', 'recipients', ['first good reason',"anyway, I don't like bar"])

    def test_reply_post_moderate(self):
        "Test 'auto_moderators' parameter."
        m = self.c21()
        pk = m.pk
        url = reverse('postman_reply', args=[pk])
        data = {'subject': 's', 'body': 'b'}
        self.assertTrue(self.client.login(username='foo', password='pass'))

        response = self.client.post(reverse('postman_reply_moderate', args=[pk]), data, HTTP_REFERER=url)
        self.assertRedirects(response, url)
        # the check_contrib_messages() in test_write_post_moderate() is enough
        self.check_status(Message.objects.get(pk=pk+1), status=STATUS_REJECTED, recipient_deleted_at=True,
            parent=m, thread=m,
            moderation_date=True, moderation_reason="some reason")

    def test_view_authentication(self):
        "Test permission, what template and form are used, set-as-read."
        template = "postman/view.html"
        pk1 = self.c12().pk
        pk2 = self.c21(body="this is my body").pk
        url = reverse('postman_view', args=[pk1])
        # anonymous
        response = self.client.get(url)
        self.assertRedirects(response, "{0}?{1}={2}".format(settings.LOGIN_URL, REDIRECT_FIELD_NAME, url))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        self.assertFalse(response.context['archived'])
        self.assertTrue(response.context['reply_to_pk'] is None)
        self.assertTrue(response.context['form'] is None)
        self.check_status(Message.objects.get(pk=pk1), status=STATUS_ACCEPTED)

        url = reverse('postman_view', args=[pk2])
        response = self.client.get(url)
        self.assertFalse(response.context['archived'])
        self.assertEqual(response.context['reply_to_pk'], pk2)
        from postman.forms import QuickReplyForm
        self.assertTrue(isinstance(response.context['form'], QuickReplyForm))
        self.assertNotContains(response, 'value="Re: s"')
        self.assertContains(response, '>\r\n</textarea>')  # as in django\forms\widgets.py\Textarea
        self.check_status(Message.objects.get(pk=pk2), status=STATUS_ACCEPTED, is_new=False)

        settings.POSTMAN_QUICKREPLY_QUOTE_BODY = True
        self.reload_modules()
        response = self.client.get(url)
        self.assertContains(response, '\n\nbar wrote:\n&gt; this is my body\n</textarea>')

    def test_view_formatters(self):
        "Test the 'formatters' parameter."
        template = "postman/view.html"
        pk = self.c21(body="this is my body").pk
        url = reverse('postman_view_formatters', args=[pk])
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        self.assertNotContains(response, 'value="Re_ s"')
        self.assertContains(response, 'bar _ this is my body</textarea>')  # POSTMAN_QUICKREPLY_QUOTE_BODY setting is not involved

    def check_view_404(self, pk):
        self.check_404('postman_view', pk)

    def test_view_id(self):
        "Test all sort of failures."
        self.assertTrue(self.client.login(username='foo', password='pass'))
        # invalid message id
        self.check_view_404(1000)
        # existent message but not yours
        self.check_view_404(Message.objects.get(pk=self.c23().pk).pk)  # create & verify really there
        # existent message but not yet visible to you
        self.check_view_404(Message.objects.get(pk=self.create(sender=self.user2, recipient=self.user1).pk).pk)

    def test_view_conversation_authentication(self):
        "Test permission, what template and form are used, number of messages in the conversation, set-as-read."
        template = "postman/view.html"
        m1 = self.c12()
        m1.read_at, m1.thread = now(), m1
        m2 = self.c21(parent=m1, thread=m1.thread, body="this is my body")
        m1.replied_at = m2.sent_at; m1.save()
        url = reverse('postman_view_conversation', args=[m1.pk])
        self.check_status(Message.objects.get(pk=m1.pk), status=STATUS_ACCEPTED, is_new=False, is_replied=True, thread=m1)
        # anonymous
        response = self.client.get(url)
        self.assertRedirects(response, "{0}?{1}={2}".format(settings.LOGIN_URL, REDIRECT_FIELD_NAME, url))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        self.assertFalse(response.context['archived'])
        self.assertEqual(response.context['reply_to_pk'], m2.pk)
        from postman.forms import QuickReplyForm
        self.assertTrue(isinstance(response.context['form'], QuickReplyForm))
        self.assertNotContains(response, 'value="Re: s"')
        self.assertContains(response, '>\r\n</textarea>')  # as in django\forms\widgets.py\Textarea
        self.assertEqual(len(response.context['pm_messages']), 2)
        self.check_status(Message.objects.get(pk=m2.pk), status=STATUS_ACCEPTED, is_new=False, parent=m1, thread=m1)

        settings.POSTMAN_QUICKREPLY_QUOTE_BODY = True
        self.reload_modules()
        response = self.client.get(url)
        self.assertContains(response, '\n\nbar wrote:\n&gt; this is my body\n</textarea>')

    def check_view_conversation_404(self, thread_id):
        self.check_404('postman_view_conversation', thread_id)

    def test_view_conversation_id(self):
        "Test all sort of failures."
        self.assertTrue(self.client.login(username='foo', password='pass'))
        # invalid conversation id
        self.check_view_conversation_404(1000)
        # existent conversation but not yours
        m1 = self.c23()
        m1.read_at, m1.thread = now(), m1
        m2 = self.c32(parent=m1, thread=m1.thread)
        m1.replied_at = m2.sent_at; m1.save()
        self.check_view_conversation_404(m1.thread_id)

    def test_view_conversation(self):
        "Test message visibility."
        m1 = self.c12()
        m1.read_at, m1.thread = now(), m1
        m1.save()
        m2 = self.create(sender=self.user2, recipient=self.user1, parent=m1, thread=m1.thread)
        url = reverse('postman_view_conversation', args=[m1.pk])
        self.check_status(Message.objects.get(pk=m1.pk), status=STATUS_ACCEPTED, is_new=False, thread=m1)
        # existent response but not yet visible to you
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.get(url)
        self.assertEqual(len(response.context['pm_messages']), 1)
        self.check_status(Message.objects.get(pk=m2.pk), parent=m1, thread=m1)
        # complete view on the other side
        self.assertTrue(self.client.login(username='bar', password='pass'))
        response = self.client.get(url)
        self.assertEqual(len(response.context['pm_messages']), 2)

    def check_update(self, view_name, success_msg, field_bit, pk, field_value=None):
        "Check permission, redirection, field updates, invalid cases."
        url = reverse(view_name)
        url_with_success_url = reverse(view_name + '_with_success_url_to_archives')
        data = {'pks': (str(pk), str(pk+1), str(pk+2))}
        # anonymous
        response = self.client.post(url, data)
        self.assertRedirects(response, "{0}?{1}={2}".format(settings.LOGIN_URL, REDIRECT_FIELD_NAME, url))
        # authenticated
        self.assertTrue(self.client.login(username='foo', password='pass'))
        # default redirect is to the requestor page
        redirect_url = reverse('postman_sent')
        response = self.client.post(url, data, HTTP_REFERER=redirect_url, follow=True)  # 'follow' to access messages
        self.assertRedirects(response, redirect_url)
        self.check_contrib_messages(response, success_msg)
        sender_kw = 'sender_{0}'.format(field_bit)
        recipient_kw = 'recipient_{0}'.format(field_bit)
        self.check_status(Message.objects.get(pk=pk),   status=STATUS_ACCEPTED, **{sender_kw: field_value})
        self.check_status(Message.objects.get(pk=pk+1), status=STATUS_ACCEPTED, **{recipient_kw: field_value})
        self.check_status(Message.objects.get(pk=pk+2), status=STATUS_ACCEPTED, **{sender_kw: field_value})
        self.check_status(Message.objects.get(pk=pk+3), status=STATUS_ACCEPTED)
        # fallback redirect is to inbox
        response = self.client.post(url, data)  # doesn't hurt if already archived|deleted|undeleted
        self.assertRedirects(response, reverse('postman_inbox'))
        # redirect url may be superseded
        response = self.client.post(url_with_success_url, data, HTTP_REFERER=redirect_url)
        self.assertRedirects(response, reverse('postman_archives'))
        # query string has highest precedence
        response = self.client.post(url_with_success_url + '?next=' + redirect_url, data, HTTP_REFERER='does not matter')
        self.assertRedirects(response, redirect_url)
        # missing payload
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('postman_inbox'))
        self.check_contrib_messages(response, 'Select at least one object.')

        # not a POST
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 405)
        # not yours
        self.assertTrue(self.client.login(username='baz', password='pass'))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def check_update_conversation(self, view_name, root_msg, field_bit, field_value=None):
        "Check redirection, field updates, invalid cases."
        url = reverse(view_name)
        pk = root_msg.pk
        data = {'tpks': str(pk)}
        self.assertTrue(self.client.login(username='foo', password='pass'))
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('postman_inbox'))
        # contrib.messages are already tested with check_update()
        sender_kw = 'sender_{0}'.format(field_bit)
        recipient_kw = 'recipient_{0}'.format(field_bit)
        self.check_status(Message.objects.get(pk=pk), status=STATUS_ACCEPTED, is_new=False, is_replied=True, thread=root_msg, **{sender_kw: field_value})
        self.check_status(Message.objects.get(pk=pk+1), status=STATUS_ACCEPTED, parent=root_msg, thread=root_msg, **{recipient_kw: field_value})
        # missing payload
        response = self.client.post(url)
        self.assertRedirects(response, reverse('postman_inbox'))

        # not a POST
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 405)
        # not yours
        self.assertTrue(self.client.login(username='baz', password='pass'))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_archive(self):
        "Test archive action on messages."
        pk = self.c12().pk
        self.c21()
        self.c12()
        self.c13()
        self.check_update('postman_archive', 'Messages or conversations successfully archived.', 'archived', pk, True)

    def test_archive_conversation(self):
        "Test archive action on conversations."
        m1 = self.c12()
        m1.read_at, m1.thread = now(), m1
        m2 = self.c21(parent=m1, thread=m1.thread)
        m1.replied_at = m2.sent_at; m1.save()
        self.check_update_conversation('postman_archive', m1, 'archived', True)

    def test_delete(self):
        "Test delete action on messages."
        pk = self.c12().pk
        self.c21()
        self.c12()
        self.c13()
        self.check_update('postman_delete', 'Messages or conversations successfully deleted.', 'deleted_at', pk, True)

    def test_delete_conversation(self):
        "Test delete action on conversations."
        m1 = self.c12()
        m1.read_at, m1.thread = now(), m1
        m2 = self.c21(parent=m1, thread=m1.thread)
        m1.replied_at = m2.sent_at; m1.save()
        self.check_update_conversation('postman_delete', m1, 'deleted_at', True)

    def test_undelete(self):
        "Test undelete action on messages."
        pk = self.c12(sender_deleted_at=now()).pk
        self.c21(recipient_deleted_at=now())
        self.c12(sender_deleted_at=now())
        self.c13()
        self.check_update('postman_undelete', 'Messages or conversations successfully recovered.', 'deleted_at', pk)

    def test_undelete_conversation(self):
        "Test undelete action on conversations."
        m1 = self.c12(sender_deleted_at=now())
        m1.read_at, m1.thread = now(), m1
        m2 = self.c21(parent=m1, thread=m1.thread, recipient_deleted_at=now())
        m1.replied_at = m2.sent_at; m1.save()
        self.check_update_conversation('postman_undelete', m1, 'deleted_at')


class FieldTest(BaseTest):
    """
    Test the CommaSeparatedUserField.
    """
    def test_label(self):
        "Test the plural/singular of the label."
        from postman.fields import CommaSeparatedUserField
        f = CommaSeparatedUserField(label=('plural','singular'))
        self.assertEqual(f.label, 'plural')
        f.set_max(1)
        self.assertEqual(f.label, 'singular')

        f = CommaSeparatedUserField(label=('plural','singular'), max=1)
        self.assertEqual(f.label, 'singular')
        f.set_max(2)
        self.assertEqual(f.label, 'plural')

        f = CommaSeparatedUserField(label=('plural','singular'), max=2)
        self.assertEqual(f.label, 'plural')
        f.set_max(1)
        self.assertEqual(f.label, 'singular')

    def test_to_python(self):
        "Test the conversion to a python list."
        from postman.fields import CommaSeparatedUserField
        f = CommaSeparatedUserField()
        self.assertEqual(f.to_python(''), [])
        self.assertEqual(f.to_python('foo'), ['foo'])
        self.assertEqual(frozenset(f.to_python('foo, bar')), frozenset(['foo', 'bar']))
        self.assertEqual(frozenset(f.to_python('foo, bar,baz')), frozenset(['foo', 'bar', 'baz']))
        self.assertEqual(f.to_python(' foo , foo '), ['foo'])
        self.assertEqual(frozenset(f.to_python('foo,, bar,')), frozenset(['foo', 'bar']))
        self.assertEqual(frozenset(f.to_python(',foo, \t , bar')), frozenset(['foo', 'bar']))

    def test_clean(self):
        "Test the 'clean' validation."
        from postman.fields import CommaSeparatedUserField
        f = CommaSeparatedUserField(required=False)
        self.assertEqual(f.clean(''), [])
        self.assertEqual(f.clean('foo'), [self.user1])
        self.assertEqual(frozenset(f.clean('foo, bar')), frozenset([self.user1, self.user2]))
        # 'intruder' is not a username
        self.assertRaises(ValidationError, f.clean, 'foo, intruder, bar')
        # only active users are considered
        self.user1.is_active = False
        self.user1.save()
        self.assertRaises(ValidationError, f.clean, 'foo, bar')

    def test_user_filter(self):
        "Test the 'user_filter' argument."
        from postman.fields import CommaSeparatedUserField
        f = CommaSeparatedUserField(user_filter=lambda u: None)
        self.assertEqual(frozenset(f.clean('foo, bar')), frozenset([self.user1, self.user2]))
        # no reason
        f = CommaSeparatedUserField(user_filter=lambda u: '' if u == self.user1 else None)
        self.assertRaises(ValidationError, f.clean, 'foo, bar')
        # with reason
        f = CommaSeparatedUserField(user_filter=lambda u: 'some reason' if u == self.user1 else None)
        self.assertRaises(ValidationError, f.clean, 'foo, bar')

    def test_min(self):
        "Test the 'min' argument."
        from postman.fields import CommaSeparatedUserField
        f = CommaSeparatedUserField(required=False, min=1)
        self.assertEqual(f.clean(''), [])

        f = CommaSeparatedUserField(min=1)
        self.assertEqual(f.clean('foo'), [self.user1])

        f = CommaSeparatedUserField(min=2)
        self.assertEqual(frozenset(f.clean('foo, bar')), frozenset([self.user1, self.user2]))
        self.assertRaises(ValidationError, f.clean, 'foo')

    def test_max(self):
        "Test the 'max' argument."
        from postman.fields import CommaSeparatedUserField
        f = CommaSeparatedUserField(max=1)
        self.assertEqual(f.clean('foo'), [self.user1])
        self.assertRaises(ValidationError, f.clean, 'foo, bar')


class MessageManagerTest(BaseTest):
    """
    Test the Message manager.
    """
    def test_num_queries(self):
        "Test the number of queries."
        # not available in django v1.2.3
        if not hasattr(self, 'assertNumQueries'):
            return
        pk = self.c12().pk
        self.c21()
        self.c12(sender_archived=True, recipient_deleted_at=now())
        self.c21(sender_archived=True, recipient_deleted_at=now())
        for u in (self.user1, self.user2):
            with self.assertNumQueries(1):
                msgs = list(Message.objects.sent(u, option=OPTION_MESSAGES))
                user = msgs[0].recipient
            with self.assertNumQueries(1):
                msgs = list(Message.objects.inbox(u, option=OPTION_MESSAGES))
                user = msgs[0].sender
            with self.assertNumQueries(1):
                msgs = list(Message.objects.archives(u, option=OPTION_MESSAGES))
                user = msgs[0].sender
                user = msgs[0].recipient
            with self.assertNumQueries(1):
                msgs = list(Message.objects.trash(u, option=OPTION_MESSAGES))
                user = msgs[0].sender
                user = msgs[0].recipient
            with self.assertNumQueries(1):
                msgs = list(Message.objects.thread(u, Q(pk=pk)))
                user = msgs[0].sender
                user = msgs[0].recipient

    def test(self):
        """
              user1       user2
        -----------       -----------  read repl
        arch del             arch del
                   ---...
                   ---X            x
                   ------>|             x    x
                  |<------|             x    x
                  |------>
                   ------>
                   ------>              x
                   <------
                    ...---
              x       X---
        """

        m1 = self.c12(moderation_status=STATUS_PENDING)
        m2 = self.c12(moderation_status=STATUS_REJECTED, recipient_deleted_at=now())
        m3 = self.c12()
        m3.read_at, m3.thread = now(), m3
        m4 = self.c21(parent=m3, thread=m3.thread)
        m3.replied_at = m4.sent_at; m3.save()
        m4.read_at = now()
        m5 = self.c12(parent=m4, thread=m4.thread)
        m4.replied_at = m5.sent_at; m4.save()
        m6 = self.c12()
        m7 = self.c12()
        m7.read_at = now(); m7.save()
        m8 = self.c21()
        m9 = self.c21(moderation_status=STATUS_PENDING)
        m10 = self.c21(moderation_status=STATUS_REJECTED, recipient_deleted_at=now())

        def pk(x): return x.pk
        def pk_cnt(x): return (x.pk, x.count)
        self.assertEqual(Message.objects.count(), 10)
        self.assertEqual(Message.objects.inbox_unread_count(self.user1), 1)
        self.assertEqual(Message.objects.inbox_unread_count(self.user2), 2)
        self.assertEqual(self.user1.sent_messages.count(), 6)
        self.assertEqual(self.user1.received_messages.count(), 4)
        self.assertEqual(self.user2.sent_messages.count(), 4)
        self.assertEqual(self.user2.received_messages.count(), 6)
        self.assertEqual(set(m3.child_messages.all()), set([m3,m4,m5]))
        self.assertEqual(list(m3.next_messages.all()), [m4])
        self.assertEqual(m3.get_replies_count(), 1)
        self.assertEqual(list(m4.next_messages.all()), [m5])
        self.assertEqual(m4.get_replies_count(), 1)
        self.assertEqual(m5.get_replies_count(), 0)
        # by messages
        self.assertQuerysetEqual(Message.objects.sent(self.user1, option=OPTION_MESSAGES), [m7.pk,m6.pk,m5.pk,m3.pk,m2.pk,m1.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.sent(self.user2, option=OPTION_MESSAGES), [m10.pk,m9.pk,m8.pk,m4.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.inbox(self.user1, option=OPTION_MESSAGES), [m8.pk,m4.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.inbox(self.user2, option=OPTION_MESSAGES), [m7.pk,m6.pk,m5.pk,m3.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.archives(self.user1, option=OPTION_MESSAGES), [], transform=pk)
        self.assertQuerysetEqual(Message.objects.archives(self.user2, option=OPTION_MESSAGES), [], transform=pk)
        self.assertQuerysetEqual(Message.objects.trash(self.user1, option=OPTION_MESSAGES), [], transform=pk)
        self.assertQuerysetEqual(Message.objects.trash(self.user2, option=OPTION_MESSAGES), [], transform=pk)
        # by conversations
        self.assertQuerysetEqual(Message.objects.sent(self.user1), [(m7.pk,0),(m6.pk,0),(m5.pk,2),(m2.pk,0),(m1.pk,0)], transform=pk_cnt)
        self.assertQuerysetEqual(Message.objects.sent(self.user2), [(m10.pk,0),(m9.pk,0),(m8.pk,0),(m4.pk,1)], transform=pk_cnt)
        self.assertQuerysetEqual(Message.objects.inbox(self.user1), [(m8.pk,0),(m4.pk,1)], transform=pk_cnt)
        self.assertQuerysetEqual(Message.objects.inbox(self.user2), [(m7.pk,0),(m6.pk,0),(m5.pk,2)], transform=pk_cnt)

        self.assertQuerysetEqual(Message.objects.thread(self.user1, Q(thread=m3.pk)), [m3.pk,m4.pk,m5.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.thread(self.user1, Q(pk=m4.pk)), [m4.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.thread(self.user2, Q(thread=m3.pk)), [m3.pk,m4.pk,m5.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.thread(self.user2, Q(pk=m4.pk)), [m4.pk], transform=pk)
        # mark as archived and deleted
        """
              user1       user2
        -----------       -----------  read repl
        arch del             arch del
         X         ---...
              X    ---X            x
         X    X    ------>|             x    x
                  |<------|   X    X    x    x
                  |------>
         X         ------>    X
                   ------>         X    x
              X    <------
                    ...---         X
              x       X---    X
        """
        m1.sender_archived = True; m1.save()
        m2.sender_deleted_at = now(); m2.save()
        m3.sender_archived, m3.sender_deleted_at = True, now(); m3.save()
        m4.sender_archived, m4.sender_deleted_at = True, now(); m4.save()
        m6.sender_archived, m6.recipient_archived = True, True; m6.save()
        m7.recipient_deleted_at = now(); m7.save()
        m8.recipient_deleted_at = now(); m8.save()
        m9.sender_deleted_at = now(); m9.save()
        m10.sender_archived = True; m10.save()
        self.assertEqual(Message.objects.inbox_unread_count(self.user1), 0)
        self.assertEqual(Message.objects.inbox_unread_count(self.user2), 1)
        # by messages
        self.assertQuerysetEqual(Message.objects.archives(self.user1, option=OPTION_MESSAGES), [m6.pk,m1.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.archives(self.user2, option=OPTION_MESSAGES), [m10.pk,m6.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.trash(self.user1, option=OPTION_MESSAGES), [m8.pk,m3.pk,m2.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.trash(self.user2, option=OPTION_MESSAGES), [m9.pk,m7.pk,m4.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.sent(self.user1, option=OPTION_MESSAGES), [m7.pk,m5.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.sent(self.user2, option=OPTION_MESSAGES), [m8.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.inbox(self.user1, option=OPTION_MESSAGES), [m4.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.inbox(self.user2, option=OPTION_MESSAGES), [m5.pk,m3.pk], transform=pk)
        # by conversations
        self.assertQuerysetEqual(Message.objects.sent(self.user1), [(m7.pk,0),(m5.pk,1)], transform=pk_cnt)
        self.assertQuerysetEqual(Message.objects.sent(self.user2), [(m8.pk,0)], transform=pk_cnt)
        self.assertQuerysetEqual(Message.objects.inbox(self.user1), [(m4.pk,1)], transform=pk_cnt)
        self.assertQuerysetEqual(Message.objects.inbox(self.user2), [(m5.pk,2)], transform=pk_cnt)

        self.assertQuerysetEqual(Message.objects.thread(self.user1, Q(thread=m3.pk)), [m3.pk,m4.pk,m5.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.thread(self.user1, Q(pk=m4.pk)), [m4.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.thread(self.user2, Q(thread=m3.pk)), [m3.pk,m4.pk,m5.pk], transform=pk)
        self.assertQuerysetEqual(Message.objects.thread(self.user2, Q(pk=m4.pk)), [m4.pk], transform=pk)
        # mark as read
        self.assertEqual(Message.objects.set_read(self.user2, Q(thread=m3.pk)), 1)
        m = Message.objects.get(pk=m5.pk)
        self.check_status(m, status=STATUS_ACCEPTED, is_new=False, parent=m4, thread=m3)
        self.check_now(m.read_at)
        self.assertEqual(Message.objects.set_read(self.user2, Q(pk=m6.pk)), 1)
        m = Message.objects.get(pk=m6.pk)
        self.check_status(m, status=STATUS_ACCEPTED, is_new=False, sender_archived=True, recipient_archived=True)
        self.check_now(m.read_at)
        self.assertEqual(Message.objects.set_read(self.user1, Q(pk=m8.pk)), 1)
        m = Message.objects.get(pk=m8.pk)
        self.check_status(m, status=STATUS_ACCEPTED, is_new=False, recipient_deleted_at=True)
        self.check_now(m.read_at)


class MessageTest(BaseTest):
    """
    Test the Message model.
    """
    def check_parties(self, m, s=None, r=None, email=''):
        "Check party related properties."
        obfuscated_email_re = re.compile('^[0-9a-f]{4}..[0-9a-f]{4}@domain$')
        m.sender, m.recipient, m.email = s, r, email
        if s or email:
            m.clean()
        else:
            self.assertRaises(ValidationError, m.clean)
        self.assertEqual(m.admin_sender(), s.get_username() if s else '<'+email+'>')
        self.assertEqual(m.clear_sender, m.admin_sender())
        if s:
            self.assertEqual(m.obfuscated_sender, s.get_username())
        elif email:
            self.assertTrue(obfuscated_email_re.match(m.obfuscated_sender))
        else:
            self.assertEqual(m.obfuscated_sender, '')
        self.assertEqual(m.admin_recipient(), r.get_username() if r else '<'+email+'>')
        self.assertEqual(m.clear_recipient, m.admin_recipient())
        if r:
            self.assertEqual(m.obfuscated_recipient, r.get_username())
        elif email:
            self.assertTrue(obfuscated_email_re.match(m.obfuscated_recipient))
        else:
            self.assertEqual(m.obfuscated_recipient, '')

    def test_parties(self):
        "Test sender/recipient/email."
        m = Message()
        self.check_parties(m)
        self.check_parties(m, s=self.user1)
        self.check_parties(m, r=self.user2)
        self.check_parties(m, s=self.user1,                   r=self.user2)
        self.check_parties(m, s=self.user1, email=self.email              )
        self.check_parties(m,               email=self.email, r=self.user2)

    def test_representation(self):
        "Test the message representation as text."
        m = Message(sender=self.user1, recipient=self.user2)
        m.subject = 'one two three four last'
        self.assertEqual(str(m), 'foo>bar:one two three four last')
        m.subject = 'one two three four last over'
        self.assertEqual(str(m), 'foo>bar:one two three four last...')

    def test_status(self):
        "Test status."
        m = Message.objects.create(subject='s')
        self.check_status(m)
        m = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED)
        self.check_status(m, status=STATUS_REJECTED)
        m = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED)
        self.check_status(m, status=STATUS_ACCEPTED)
        m = Message.objects.create(subject='s', read_at=now())
        self.check_status(m, is_new=False)
        m = Message.objects.create(subject='s', replied_at=now())
        self.check_status(m, is_replied=True)

    def test_moderated_count(self):
        "Test 'moderated_messages' count."
        msg = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED,
            moderation_date=now(), moderation_by=self.user1)
        msg.save()
        self.assertEqual(list(self.user1.moderated_messages.all()), [msg])

    def test_moderation_from_pending(self):
        "Test moderation management when leaving 'pending' status."
        msg = Message.objects.create(subject='s')
        # pending -> pending: nothing changes
        m = copy.copy(msg)
        m.clean_moderation(STATUS_PENDING, self.user1)
        self.check_status(m)
        # pending -> rejected
        m = copy.copy(msg)
        m.moderation_status = STATUS_REJECTED
        m.clean_moderation(STATUS_PENDING, self.user1)  # one try with moderator
        self.check_status(m, status=STATUS_REJECTED,
            moderation_date=True, moderation_by=self.user1, recipient_deleted_at=True)
        self.check_now(m.moderation_date)
        self.check_now(m.recipient_deleted_at)
        # pending -> accepted
        m = copy.copy(msg)
        m.moderation_status = STATUS_ACCEPTED
        m.clean_moderation(STATUS_PENDING)  # one try without moderator
        self.check_status(m, status=STATUS_ACCEPTED, moderation_date=True)
        self.check_now(m.moderation_date)

    def test_moderation_from_rejected(self):
        "Test moderation management when leaving 'rejected' status."
        date_in_past = now() - timedelta(days=2)  # any value, just to avoid now()
        reason = 'some good reason'
        msg = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED,
            moderation_date=date_in_past, moderation_by=self.user1, moderation_reason=reason,
            recipient_deleted_at=date_in_past)
        # rejected -> rejected: nothing changes
        m = copy.copy(msg)
        m.clean_moderation(STATUS_REJECTED, self.user2)
        self.check_status(m, status=STATUS_REJECTED,
            moderation_date=date_in_past, moderation_by=self.user1, moderation_reason=reason,
            recipient_deleted_at=date_in_past)
        # rejected -> pending
        m = copy.copy(msg)
        m.moderation_status = STATUS_PENDING
        m.clean_moderation(STATUS_REJECTED)  # one try without moderator
        self.check_status(m, status=STATUS_PENDING,
            moderation_date=True, moderation_reason=reason, recipient_deleted_at=False)
        self.check_now(m.moderation_date)
        # rejected -> accepted
        m = copy.copy(msg)
        m.moderation_status = STATUS_ACCEPTED
        m.clean_moderation(STATUS_REJECTED, self.user2)  # one try with moderator
        self.check_status(m, status=STATUS_ACCEPTED,
            moderation_date=True, moderation_by=self.user2, moderation_reason=reason,
            recipient_deleted_at=False)
        self.check_now(m.moderation_date)

    def test_moderation_from_accepted(self):
        "Test moderation management when leaving 'accepted' status."
        date_in_past = now() - timedelta(days=2)  # any value, just to avoid now()
        msg = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED,
            moderation_date=date_in_past, moderation_by=self.user1, recipient_deleted_at=date_in_past)
        # accepted -> accepted: nothing changes
        m = copy.copy(msg)
        m.clean_moderation(STATUS_ACCEPTED, self.user2)
        self.check_status(m, status=STATUS_ACCEPTED,
            moderation_date=date_in_past, moderation_by=self.user1, recipient_deleted_at=date_in_past)
        # accepted -> pending
        m = copy.copy(msg)
        m.moderation_status = STATUS_PENDING
        m.clean_moderation(STATUS_ACCEPTED, self.user2)  # one try with moderator
        self.check_status(m, status=STATUS_PENDING,
            moderation_date=True, moderation_by=self.user2, recipient_deleted_at=date_in_past)
        self.check_now(m.moderation_date)
        # accepted -> rejected
        m = copy.copy(msg)
        m.moderation_status = STATUS_REJECTED
        m.clean_moderation(STATUS_ACCEPTED)  # one try without moderator
        self.check_status(m, status=STATUS_REJECTED, moderation_date=True, recipient_deleted_at=True)
        self.check_now(m.moderation_date)
        self.check_now(m.recipient_deleted_at)

    def test_visitor(self):
        "Test clean_for_visitor()."
        date_in_past = now() - timedelta(days=2)  # any value, just to avoid now()
        # as the sender
        m = Message.objects.create(subject='s', recipient=self.user1)
        m.clean_for_visitor()
        self.check_status(m, sender_deleted_at=True)
        self.check_now(m.sender_deleted_at)
        # as the recipient
        msg = Message.objects.create(subject='s', sender=self.user1)
        # pending
        m = copy.copy(msg)
        m.read_at=date_in_past
        m.recipient_deleted_at=date_in_past
        m.clean_for_visitor()
        self.check_status(m, recipient_deleted_at=False)
        # rejected
        m = copy.copy(msg)
        m.moderation_status = STATUS_REJECTED
        m.read_at=date_in_past
        m.recipient_deleted_at=date_in_past
        m.clean_for_visitor()
        self.check_status(m, status=STATUS_REJECTED, recipient_deleted_at=date_in_past)
        # accepted
        m = copy.copy(msg)
        m.moderation_status = STATUS_ACCEPTED
        m.clean_for_visitor()
        self.check_status(m, status=STATUS_ACCEPTED, is_new=False, recipient_deleted_at=True)
        self.check_now(m.read_at)
        self.check_now(m.recipient_deleted_at)

    def test_update_parent(self):
        "Test update_parent()."
        parent = Message.objects.create(subject='s', sender=self.user1, recipient=self.user2,
            moderation_status=STATUS_ACCEPTED)
        parent.thread = parent
        parent.save()
        # any previous rejected reply should not interfere
        rejected_reply = Message.objects.create(subject='s', sender=self.user2, recipient=self.user1,
            parent=parent, thread=parent.thread, moderation_status=STATUS_REJECTED)
        # any previous pending reply should not interfere
        pending_reply = Message.objects.create(subject='s', sender=self.user2, recipient=self.user1,
            parent=parent, thread=parent.thread, moderation_status=STATUS_PENDING)
        reply = Message.objects.create(subject='s', sender=self.user2, recipient=self.user1,
            parent=parent, thread=parent.thread)

        # the reply is accepted
        r = copy.deepcopy(reply)
        r.moderation_status = STATUS_ACCEPTED
        # accepted -> accepted: no change
        r.update_parent(STATUS_ACCEPTED)
        self.check_status(r.parent, status=STATUS_ACCEPTED, thread=parent)
        # pending -> accepted: parent is replied
        r.update_parent(STATUS_PENDING)
        p = Message.objects.get(pk=parent.pk)  # better to ask the DB to check the save()
        self.check_status(p, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        self.assertEqual(p.replied_at.timetuple(), r.sent_at.timetuple())  # mysql doesn't store microseconds
        # rejected -> accepted: same as pending -> accepted
        # so check here the acceptance of an anterior date
        # note: use again the some object for convenience but another reply is more realistic
        r.sent_at = r.sent_at - timedelta(days=1)
        r.update_parent(STATUS_REJECTED)
        p = Message.objects.get(pk=parent.pk)
        self.check_status(p, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        self.assertEqual(p.replied_at.timetuple(), r.sent_at.timetuple())

        # a reply is withdrawn and no other reply
        r = copy.deepcopy(reply)
        r.parent.replied_at = r.sent_at
        r.moderation_status = STATUS_REJECTED  # could be STATUS_PENDING
        # rejected -> rejected: no change. In real case, parent.replied_at would be already empty
        r.update_parent(STATUS_REJECTED)
        self.check_status(r.parent, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        # pending -> rejected: no change. In real case, parent.replied_at would be already empty
        r.update_parent(STATUS_PENDING)
        self.check_status(r.parent, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        # accepted -> rejected: parent is no more replied
        r.update_parent(STATUS_ACCEPTED)
        p = Message.objects.get(pk=parent.pk)
        self.check_status(p, status=STATUS_ACCEPTED, thread=parent)
        # note: accepted -> rejected, with the existence of another suitable reply
        # is covered in the accepted -> pending case

        # a reply is withdrawn but there is another suitable reply
        other_reply = Message.objects.create(subject='s', sender=self.user2, recipient=self.user1,
            parent=parent, thread=parent.thread, moderation_status=STATUS_ACCEPTED)
        r = copy.deepcopy(reply)
        r.parent.replied_at = r.sent_at
        r.moderation_status = STATUS_PENDING  # could be STATUS_REJECTED
        # pending -> pending: no change. In real case, parent.replied_at would be from another reply object
        r.update_parent(STATUS_PENDING)
        self.check_status(r.parent, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        # rejected -> pending: no change. In real case, parent.replied_at would be from another reply object
        r.update_parent(STATUS_REJECTED)
        self.check_status(r.parent, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        # accepted -> pending: parent is still replied but by another object
        r.update_parent(STATUS_ACCEPTED)
        p = Message.objects.get(pk=parent.pk)
        self.check_status(p, status=STATUS_ACCEPTED, thread=parent, is_replied=True)
        self.assertEqual(p.replied_at.timetuple(), other_reply.sent_at.timetuple())
        # note: accepted -> pending, with no other suitable reply
        # is covered in the accepted -> rejected case

    def check_notification(self, m, mail_number, email=None, is_auto_moderated=True, notice_label=None):
        "Check number of mails, recipient, and notice creation."
        m.notify_users(STATUS_PENDING, Site.objects.get_current() if Site._meta.installed else None, is_auto_moderated)
        self.assertEqual(len(mail.outbox), mail_number)
        if mail_number:
            self.assertEqual(mail.outbox[0].to, [email])
        from postman.utils import notification
        if notification and notice_label:
            if hasattr(notification, "Notice"):  # exists for django-notification 0.2.0, but no more in 1.0
                notice = notification.Notice.objects.get()
                self.assertEqual(notice.notice_type.label, notice_label)

    def test_notification_rejection_visitor(self):
        "Test notify_users() for rejection, sender is a visitor."
        m = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED, email=self.email, recipient=self.user2)
        self.check_notification(m, 1, self.email)

    def test_notification_rejection_user(self):
        "Test notify_users() for rejection, sender is a User."
        m = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED, sender=self.user1, recipient=self.user2)
        self.check_notification(m, 1, self.user1.email, is_auto_moderated=False, notice_label='postman_rejection')

    def test_notification_rejection_user_auto_moderated(self):
        "Test notify_users() for rejection, sender is a User, and is alerted online."
        m = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED, sender=self.user1, recipient=self.user2)
        self.check_notification(m, 0, is_auto_moderated=True)

    def test_notification_rejection_user_inactive(self):
        "Test notify_users() for rejection, sender is a User, but must be active."
        m = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED, sender=self.user1, recipient=self.user2)
        self.user1.is_active = False
        self.check_notification(m, 0, is_auto_moderated=False, notice_label='postman_rejection')

    def test_notification_rejection_user_disable(self):
        "Test notify_users() for rejection, sender is a User, but emailing is disabled."
        m = Message.objects.create(subject='s', moderation_status=STATUS_REJECTED, sender=self.user1, recipient=self.user2)
        settings.POSTMAN_DISABLE_USER_EMAILING = True
        settings.POSTMAN_NOTIFIER_APP = None
        self.reload_modules()
        self.check_notification(m, 0, is_auto_moderated=False)

    def test_notification_acceptance_visitor(self):
        "Test notify_users() for acceptance, recipient is a visitor."
        m = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED, sender=self.user1, email=self.email)
        self.check_notification(m, 1, self.email)

    def test_notification_acceptance_user(self):
        "Test notify_users() for acceptance, recipient is a User."
        m = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED, sender=self.user1, recipient=self.user2)
        self.check_notification(m, 1, self.user2.email, notice_label='postman_message')

    def test_notification_acceptance_user_inactive(self):
        "Test notify_users() for acceptance, recipient is a User, but must be active."
        m = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED, sender=self.user1, recipient=self.user2)
        self.user2.is_active = False
        self.check_notification(m, 0, notice_label='postman_message')

    def test_notification_acceptance_user_disable(self):
        "Test notify_users() for acceptance, recipient is a User, but emailing is disabled."
        m = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED, sender=self.user1, recipient=self.user2)
        settings.POSTMAN_DISABLE_USER_EMAILING = True
        settings.POSTMAN_NOTIFIER_APP = None
        self.reload_modules()
        self.check_notification(m, 0, notice_label='postman_message')

    def test_notification_acceptance_reply(self):
        "Test notify_users() for acceptance, for a reply, recipient is a User."
        p = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED, sender=self.user2, recipient=self.user1)
        m = Message.objects.create(subject='s', moderation_status=STATUS_ACCEPTED, sender=self.user1, recipient=self.user2,
            parent=p, thread=p)
        self.check_notification(m, 1, self.user2.email, notice_label='postman_reply')

    def test_dates(self):
        "Test set_dates(), get_dates()."
        m = Message()
        set = now(), now(), now()
        m.set_dates(*set)
        get = m.get_dates()
        self.assertEqual(get, set)

    def test_moderation(self):
        "Test set_moderation(), get_moderation()."
        m = Message()
        set = STATUS_ACCEPTED, self.user1.pk, now(), 'some reason'
        m.set_moderation(*set)
        get = m.get_moderation()
        self.assertEqual(get, set)

    def check_auto_moderation(self, msg, seq, default):
        "Check auto-moderation results."
        for mod, result in seq:
            m = copy.copy(msg)
            m.auto_moderate(mod)
            changes = {}
            if result is True:
                changes['status'] = STATUS_ACCEPTED
            elif result is None:
                changes['status'] = default
            else:
                changes['status'] = STATUS_REJECTED
                changes['moderation_reason'] = result
            m.sent_at = now()  # refresh, as we recycle the same base message
            self.check_status(m, **changes)

    def test_auto_moderation(self):
        "Test auto-moderation function combination."
        msg = Message.objects.create(subject='s')

        def moderate_as_none(m):              return None
        def moderate_as_true(m):              return True
        def moderate_as_false(m):             return False
        def moderate_as_0(m):                 return 0
        def moderate_as_100(m):               return 100
        def moderate_as_50(m):                return 50
        def moderate_as_49_default_reason(m): return 49
        moderate_as_49_default_reason.default_reason = 'moderate_as_49 default_reason'
        def moderate_as_49_with_reason(m):    return (49, 'moderate_as_49 with_reason')
        moderate_as_49_with_reason.default_reason = 'is not used'
        def moderate_as_1(m):                 return (1, 'moderate_as_1')
        def moderate_as_1_no_reason(m):       return (1, ' ')
        def moderate_as_2(m):                 return (2, 'moderate_as_2')
        def moderate_as_98(m):                return 98
        moderate_as_98.default_reason = 'useless; never used'
        def moderate_badly_as_negative(m):    return -1
        def moderate_badly_as_too_high(m):    return 101
        def moderate_as_0_with_reason(m):     return (0, 'moderate_as_0 with_reason')
        def invalid_moderator_1(m):           return (0, )
        def invalid_moderator_2(m):           return (0, 'reason', 'extra')

        for mod in [invalid_moderator_1, invalid_moderator_2]:
            m = copy.copy(msg)
            self.assertRaises(ValueError, m.auto_moderate, mod)

        seq = (
            # no moderator, no valid rating, or moderator is unable to state, default applies
            ([], None),
            (moderate_badly_as_negative, None),
            (moderate_badly_as_too_high, None),
            (moderate_as_none, None),
            # firm decision
            (moderate_as_false, ''),  (moderate_as_0, ''),
            (moderate_as_true, True), (moderate_as_100, True),
            # round to up
            (moderate_as_50, True),
            # reasons
            (moderate_as_49_default_reason, moderate_as_49_default_reason.default_reason),
            (moderate_as_49_with_reason, 'moderate_as_49 with_reason'),
            # priority is left to right
            ([moderate_as_none, moderate_as_false, moderate_as_true], ''),
            ([moderate_as_none, moderate_as_true, moderate_as_false], True),
            # keep only reasons for ratings below 50, non empty or whitespace
            ([moderate_as_1, moderate_as_98], 'moderate_as_1'),
            ([moderate_as_1, moderate_as_2, moderate_as_50], 'moderate_as_1, moderate_as_2'),
            ([moderate_as_1, moderate_as_1_no_reason, moderate_as_2], 'moderate_as_1, moderate_as_2'),
            # a firm reject imposes its reason
            ([moderate_as_1, moderate_as_2, moderate_as_50, moderate_as_0_with_reason], 'moderate_as_0 with_reason'),
            # neutral or invalid moderators do not count in the average
            ([moderate_as_50, moderate_as_none, moderate_badly_as_negative, moderate_badly_as_too_high], True),
        )
        # no default auto moderation
        # settings.POSTMAN_AUTO_MODERATE_AS = None
        self.check_auto_moderation(msg, seq, STATUS_PENDING)
        # default is: accepted
        settings.POSTMAN_AUTO_MODERATE_AS = True
        self.check_auto_moderation(msg, seq, STATUS_ACCEPTED)
        # default is: rejected
        settings.POSTMAN_AUTO_MODERATE_AS = False
        self.check_auto_moderation(msg, seq, STATUS_REJECTED)


class PendingMessageManagerTest(BaseTest):
    """
    Test the PendingMessage manager.
    """
    def test(self):
        msg1 = self.create()
        msg2 = self.create(moderation_status=STATUS_REJECTED)
        msg3 = self.create(moderation_status=STATUS_ACCEPTED)
        msg4 = self.create()
        self.assertQuerysetEqual(PendingMessage.objects.all(), [msg4.pk, msg1.pk], transform=lambda x: x.pk)


class PendingMessageTest(BaseTest):
    """
    Test the PendingMessage model.
    """
    def test(self):
        m = PendingMessage()
        self.assertTrue(m.is_pending())
        m.set_accepted()
        self.assertTrue(m.is_accepted())
        m.set_rejected()
        self.assertTrue(m.is_rejected())


class FiltersTest(BaseTest):
    """
    Test the filters.
    """
    def check_sub(self, x, y, value):
        t = Template("{% load postman_tags %}{% with "+x+"|sub:"+y+" as var %}{{ var }}{% endwith %}")
        self.assertEqual(t.render(Context({})), value)

    def test_sub(self):
        "Test '|sub'."
        self.check_sub('6', '2', '4')
        self.check_sub('6', "'X'", '6')
        self.check_sub("'X'", '2', 'X')

    def check_or_me(self, x, value, user=None, m=None):
        t = Template("{% load postman_tags %}{{ "+x+"|or_me:user }}")  # do not load i18n to be able to check the untranslated pattern
        self.assertEqual(t.render(Context({'user': user or AnonymousUser(), 'message': m})), value)

    def test_or_me(self):
        "Test '|or_me'."
        self.check_or_me("'foo'", 'foo')
        self.check_or_me("'foo'", '&lt;me&gt;', self.user1)
        self.check_or_me("'bar'", 'bar', self.user1)
        self.check_or_me("user", '&lt;me&gt;', self.user1)
        m = self.c12()
        self.check_or_me("message.obfuscated_sender", '&lt;me&gt;', self.user1, m=m)
        self.check_or_me("message.obfuscated_recipient", 'bar', self.user1, m=m)
        settings.POSTMAN_SHOW_USER_AS = 'email'
        self.check_or_me("message.obfuscated_sender", '&lt;me&gt;', self.user1, m=m)
        self.check_or_me("message.obfuscated_recipient", 'bar@domain.com', self.user1, m=m)

    def check_compact_date(self, date, value, format='H:i,d b,d/m/y'):
        # use 'H', 'd', 'm' instead of 'G', 'j', 'n' because no strftime equivalents
        t = Template('{% load postman_tags %}{{ date|compact_date:"'+format+'" }}')
        self.assertEqual(t.render(Context({'date': date})), value)

    def test_compact_date(self):
        "Test '|compact_date'."
        dt = now()
        try:
            from django.utils.timezone import localtime  # Django 1.4 aware datetimes
            # (1.4) template/base.py/_render_value_in_context()
            dt = localtime(dt)
        except ImportError:
            pass
        # (1.2) template/__init__.py/_render_value_in_context()
        # (1.3) template/base.py/_render_value_in_context()
        # (1.6) template/base.py/render_value_in_context()
        default = force_text(localize(dt))

        self.check_compact_date(dt, default, format='')
        self.check_compact_date(dt, default, format='one')
        self.check_compact_date(dt, default, format='one,two')
        self.check_compact_date(dt, dt.strftime('%H:%M'))
        dt2 = dt - timedelta(days=1)  # little fail: do not work on Jan, 1st, because the year changes as well
        self.check_compact_date(dt2, dt2.strftime('%d %b').lower())  # filter's 'b' is lowercase
        dt2 = dt - timedelta(days=365)
        self.check_compact_date(dt2, dt2.strftime('%d/%m/%y'))


class TagsTest(BaseTest):
    """
    Test the template tags.
    """
    def check_postman_unread(self, value, user=None, asvar=''):
        t = Template("{% load postman_tags %}{% postman_unread " + asvar +" %}")
        ctx = Context({'user': user} if user else {})
        self.assertEqual(t.render(ctx), value)
        return ctx

    def test_postman_unread(self):
        "Test 'postman_unread'."
        self.check_postman_unread('')
        self.check_postman_unread('', AnonymousUser())
        self.check_postman_unread('0', self.user1)
        Message.objects.create(subject='s', recipient=self.user1)
        self.check_postman_unread('0', self.user1)
        Message.objects.create(subject='s', recipient=self.user1, moderation_status=STATUS_ACCEPTED)
        self.check_postman_unread('1', self.user1)
        ctx = self.check_postman_unread('', self.user1, 'as var')
        self.assertEqual(ctx['var'], 1)
        self.assertRaises(TemplateSyntaxError, self.check_postman_unread, '', self.user1, 'as var extra')
        self.assertRaises(TemplateSyntaxError, self.check_postman_unread, '', self.user1, 'As var')

    def check_order_by(self, keyword, value_list, context=None):
        t = Template("{% load postman_tags %}{% postman_order_by " + keyword +" %}")
        r = t.render(Context({'gets': QueryDict(context)} if context else {}))
        self.assertEqual(r[0], '?')
        self.assertEqual(set(r[1:].split('&')), set([k+'='+v for k, v in value_list]))

    def test_order_by(self):
        "Test 'postman_order_by'."
        for k, v in ORDER_BY_MAPPER.items():
            self.check_order_by(k, [(ORDER_BY_KEY, v)])
        self.check_order_by('subject', [(ORDER_BY_KEY, 's')], ORDER_BY_KEY+'=foo')
        self.check_order_by('subject', [(ORDER_BY_KEY, 'S')], ORDER_BY_KEY+'=s')
        self.check_order_by('subject', [(ORDER_BY_KEY, 's'), ('page', '12')], 'page=12')
        self.check_order_by('subject', [('foo', 'bar'), (ORDER_BY_KEY, 's'), ('baz', 'qux')], 'foo=bar&'+ORDER_BY_KEY+'=S&baz=qux')
        self.assertRaises(TemplateSyntaxError, self.check_order_by, '', None)
        self.assertRaises(TemplateSyntaxError, self.check_order_by, 'subject extra', None)
        self.assertRaises(TemplateSyntaxError, self.check_order_by, 'unknown', None)


class UtilsTest(BaseTest):
    """
    Test helper functions.
    """
    def test_format_body(self):
        "Test format_body()."
        header = "\n\nfoo wrote:\n"
        footer = "\n"
        self.assertEqual(format_body(self.user1, "foo bar"), header+"> foo bar"+footer)
        self.assertEqual(format_body(self.user1, "foo bar", indent='|_'), header+"|_foo bar"+footer)
        self.assertEqual(format_body(self.user1, width=10, body="34 67 90"), header+"> 34 67 90"+footer)
        self.assertEqual(format_body(self.user1, width=10, body="34 67 901"), header+"> 34 67\n> 901"+footer)
        self.assertEqual(format_body(self.user1, width=10, body="> 34 67 901"), header+"> > 34 67 901"+footer)
        self.assertEqual(format_body(self.user1, width=10,
            body=    "34 67\n"   "\n" "  \n"   "  .\n"   "End"),
            header+"> 34 67\n" "> \n" "> \n" ">   .\n" "> End"+footer)

    def test_format_subject(self):
        "Test format_subject()."
        self.assertEqual(format_subject("foo bar"), "Re: foo bar")
        self.assertEqual(format_subject("Re: foo bar"), "Re: foo bar")
        self.assertEqual(format_subject("rE: foo bar"), "rE: foo bar")

    def test_get_order_by(self):
        "Test get_order_by()."
        self.assertEqual(get_order_by({}), None)
        self.assertEqual(get_order_by({ORDER_BY_KEY: 'f'}), 'sender__{0}'.format(get_user_model().USERNAME_FIELD))
        self.assertEqual(get_order_by({ORDER_BY_KEY: 'D'}), '-sent_at')

    def test_get_user_representation(self):
        "Test get_user_representation()."
        # no setting
        self.assertEqual(get_user_representation(self.user1), "foo")
        # a wrong setting
        settings.POSTMAN_SHOW_USER_AS = 'unknown_attribute'
        self.assertEqual(get_user_representation(self.user1), "foo")
        # a valid setting but an empty attribute
        settings.POSTMAN_SHOW_USER_AS = 'first_name'
        self.assertEqual(get_user_representation(self.user1), "foo")
        # a property name
        settings.POSTMAN_SHOW_USER_AS = 'email'
        self.assertEqual(get_user_representation(self.user1), "foo@domain.com")
        if not six.PY3:  # avoid six.PY2, not available in six 1.2.0
            settings.POSTMAN_SHOW_USER_AS = b'email'  # usage on PY3 is nonsense
            self.assertEqual(get_user_representation(self.user1), "foo@domain.com")
        # a method name
        # can't use get_full_name(), an empty string in our case
        # get_absolute_url() doesn't exist anymore since Django 1.7
        settings.POSTMAN_SHOW_USER_AS = 'natural_key'  # avoid get_username(), already used for the default representation
        self.assertEqual(get_user_representation(self.user1), "(u'foo',)" if not six.PY3 else "('foo',)")
        # a function
        settings.POSTMAN_SHOW_USER_AS = lambda u: u.natural_key()
        self.assertEqual(get_user_representation(self.user1), "(u'foo',)" if not six.PY3 else "('foo',)")


class ApiTest(BaseTest):
    """
    Test the API functions.
    """
    def check_message(self, m, subject='s', body='b', recipient_username='bar'):
        "Check some message properties."
        self.assertEqual(m.subject, subject)
        self.assertEqual(m.body, body)
        self.assertEqual(m.email, '')
        self.assertEqual(m.sender, self.user1)
        self.assertEqual(m.recipient.get_username(), recipient_username)

    def test_pm_broadcast(self):
        "Test the case of a single recipient."
        pm_broadcast(sender=self.user1, recipients=self.user2, subject='s', body='b')
        m = Message.objects.get()
        self.check_status(m, status=STATUS_ACCEPTED, moderation_date=True,
            sender_archived=True, sender_deleted_at=True)
        self.check_now(m.sender_deleted_at)
        self.check_now(m.moderation_date)
        self.check_message(m)
        self.assertEqual(len(mail.outbox), 1)

    def test_pm_broadcast_skip_notification(self):
        "Test the notification skipping."
        pm_broadcast(sender=self.user1, recipients=self.user2, subject='s', skip_notification=True)
        self.assertEqual(len(mail.outbox), 0)

    def test_pm_broadcast_multi(self):
        "Test the case of more than a single recipient."
        pm_broadcast(sender=self.user1, recipients=[self.user2, self.user3], subject='s', body='b')
        msgs = list(Message.objects.all())
        self.check_message(msgs[0], recipient_username='baz')
        self.check_message(msgs[1])

    def test_pm_write(self):
        "Test the basic minimal use."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', body='b')
        m = Message.objects.get()
        self.check_status(m, status=STATUS_ACCEPTED, moderation_date=True)
        self.check_now(m.moderation_date)
        self.check_message(m)
        self.assertEqual(len(mail.outbox), 1)  # notify the recipient

    def test_pm_write_skip_notification(self):
        "Test the notification skipping."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', skip_notification=True)
        self.assertEqual(len(mail.outbox), 0)

    def test_pm_write_auto_archive(self):
        "Test the auto_archive parameter."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', auto_archive=True)
        m = Message.objects.get()
        self.check_status(m, status=STATUS_ACCEPTED, moderation_date=True, sender_archived=True)

    def test_pm_write_auto_delete(self):
        "Test the auto_delete parameter."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', auto_delete=True)
        m = Message.objects.get()
        self.check_status(m, status=STATUS_ACCEPTED, moderation_date=True, sender_deleted_at=True)
        self.check_now(m.sender_deleted_at)

    def test_pm_write_auto_moderators_accepted(self):
        "Test the auto_moderators parameter, moderate as accepted."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', auto_moderators=lambda m: True)
        m = Message.objects.get()
        self.check_status(m, status=STATUS_ACCEPTED, moderation_date=True)

    def test_pm_write_auto_moderators_pending(self):
        "Test the auto_moderators parameter, no moderation decision is taken. Test the parameter as a list."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', auto_moderators=[lambda m: None])
        m = Message.objects.get()
        self.check_status(m)
        self.assertEqual(len(mail.outbox), 0)  # no one to notify

    def test_pm_write_auto_moderators_rejected(self):
        "Test the auto_moderators parameter, moderate as rejected. Test the parameter as a tuple."
        pm_write(sender=self.user1, recipient=self.user2, subject='s', auto_moderators=(lambda m: False, ))
        m = Message.objects.get()
        self.check_status(m, status=STATUS_REJECTED, moderation_date=True, recipient_deleted_at=True)
        self.check_now(m.moderation_date)
        self.check_now(m.recipient_deleted_at)
        self.assertEqual(len(mail.outbox), 0)  # sender is not notified in the case of auto moderation
