"""
A mock of django-pagination's pagination_tags.py that does nothing.

'pagination_tags' is a name from the django-pagination application.
For convenience, the design of the default template set is done with the use of that application.
This mock will avoid failures in template rendering if the real application is not installed,
as it may be the case for the test suite run in a minimal configuration.

To deactivate this mock and use the real implementation, just make sure that 'pagination' is declared
before 'postman' in the INSTALLED_APPS setting.
"""
from __future__ import unicode_literals

from django.template import Node, Library

register = Library()


class AutoPaginateNode(Node):
    def render(self, context):
        return ''


@register.tag
def autopaginate(parser, token):
    return AutoPaginateNode()


class PaginateNode(Node):
    def render(self, context):
        return ''


@register.tag
def paginate(parser, token):
    return PaginateNode()
