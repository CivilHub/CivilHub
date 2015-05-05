from __future__ import unicode_literals
import datetime

from django import VERSION
try:
    from django.contrib.auth import get_user_model  # Django 1.5
except ImportError:
    from postman.future_1_5 import get_user_model
from django.http import QueryDict
from django.template import Node
from django.template import TemplateSyntaxError
from django.template import Library
from django.template.defaultfilters import date
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from postman.models import ORDER_BY_KEY, ORDER_BY_MAPPER, Message,\
    get_user_representation

register = Library()


##########
# filters
##########
@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value
sub.is_safe = True


@register.filter
def or_me(value, arg):
    """
    Replace the value by a fixed pattern, if it equals the argument.

    Typical usage: message.obfuscated_sender|or_me:user

    """
    user_model = get_user_model()
    if not isinstance(value, six.string_types):
        value = (get_user_representation if isinstance(value, user_model) else force_text)(value)
    if not isinstance(arg, six.string_types):
        arg = (get_user_representation if isinstance(arg, user_model) else force_text)(arg)
    return _('<me>') if value == arg else value


@register.filter(**({'expects_localtime': True, 'is_safe': False} if VERSION >= (1, 4) else {}))
def compact_date(value, arg):
    """
    Output a date as short as possible.

    The argument must provide 3 patterns: for same day, for same year, otherwise
    Typical usage: |compact_date:_("G:i,j b,j/n/y")

    """
    bits = arg.split(',')
    if len(bits) < 3:
        return value  # Invalid arg.
    today = datetime.date.today()
    return date(value, bits[0] if value.date() == today else bits[1] if value.year == today.year else bits[2])


#######
# tags
#######
class OrderByNode(Node):
    "For use in the postman_order_by tag"
    def __init__(self, code):
        self.code = code

    def render(self, context):
        """
        Return a formatted GET query string, as "?order_key=order_val".

        Preserves existing GET's keys, if any, such as a page number.
        For that, the view has to provide request.GET in a 'gets' entry of the context.

        """
        if 'gets' in context:
            gets = context['gets'].copy()
        else:
            gets = QueryDict('').copy()
        if ORDER_BY_KEY in gets:
            code = gets.pop(ORDER_BY_KEY)[0]
        else:
            code = None
        if self.code:
            gets[ORDER_BY_KEY] = self.code if self.code != code else self.code.upper()
        return '?'+gets.urlencode() if gets else ''


class InboxCountNode(Node):
    "For use in the postman_unread tag"
    def __init__(self, asvar=None):
        self.asvar = asvar

    def render(self, context):
        """
        Return the count of unread messages for the user found in context,
        (may be 0) or an empty string.
        """
        try:
            user = context['user']
            if user.is_anonymous():
                count = ''
            else:
                count = Message.objects.inbox_unread_count(user)
        except (KeyError, AttributeError):
            count = ''
        if self.asvar:
            context[self.asvar] = count
            return ''
        return count


@register.tag
def postman_order_by(parser, token):
    """
    Compose a query string to ask for a specific ordering in messages list.

    The unique argument must be one of the keywords of a set defined in the model.
    Example::

        <a href="{% postman_order_by subject %}">...</a>
    """
    try:
        tag_name, field_name = token.split_contents()
        field_code = ORDER_BY_MAPPER[field_name.lower()]
    except ValueError:
        raise TemplateSyntaxError("'{0}' tag requires a single argument".format(token.contents.split()[0]))
    except KeyError:
        raise TemplateSyntaxError(
            "'{0}' is not a valid argument to '{1}' tag."
            " Must be one of: {2}".format(field_name, tag_name, ORDER_BY_MAPPER.keys()))
    return OrderByNode(field_code)


@register.tag
def postman_unread(parser, token):
    """
    Give the number of unread messages for a user,
    or nothing (an empty string) for an anonymous user.

    Storing the count in a variable for further processing is advised, such as::

        {% postman_unread as unread_count %}
        ...
        {% if unread_count %}
            You have <strong>{{ unread_count }}</strong> unread messages.
        {% endif %}
    """
    bits = token.split_contents()
    if len(bits) > 1:
        if len(bits) != 3:
            raise TemplateSyntaxError("'{0}' tag takes no argument or exactly two arguments".format(bits[0]))
        if bits[1] != 'as':
            raise TemplateSyntaxError("First argument to '{0}' tag must be 'as'".format(bits[0]))
        return InboxCountNode(bits[2])
    else:
        return InboxCountNode()
