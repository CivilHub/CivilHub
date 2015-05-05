"""
Written as in contrib/admin/templatetags/admin_modify.py,
to define a customized version of 'submit_row' tag with a cutomized html template.

In use in templates/admin/postman/pendingmessage/change_form.html.
"""
from __future__ import unicode_literals

from django import template

register = template.Library()


@register.inclusion_tag('admin/postman/pendingmessage/submit_line.html')
def postman_submit_row():
    return {}
