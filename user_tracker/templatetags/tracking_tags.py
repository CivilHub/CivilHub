# -*- coding: utf-8 -*-
from django import template

from .models import Visitor


class VisitorsOnSite(template.Node):
    """
    Inject the number of active users on your site as an integer
    into the context.
    """
    def __init__(self, varname, same_page=False):
        self.varname = varname
        self.same_page = same_page

    def render(self, context):
        if self.same_page:
            try:
                url = context['request'].path
                count = Visitor.objects.active().filter(url=url).count()
            except KeyError:
                raise template.TemplateSyntaxError(
                    "Please add 'django.core.context_processors.request' "
                    "to your TEMPLATE_CONTEXT_PROCESSORS if you want to "
                    "see how many users are on the same page.")
        else:
            count = Visitor.objects.active().count()

        context[self.varname] = count
        return ''


def visitors_on_site(parser, token):
    """
    Determines the number of active users on your site and puts it
    into the context
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'visitors_on_site usage: {% visitors_on_site as visitors %}')

    return VisitorsOnSite(varname)


def visitors_on_page(parser, token):
    """
    Determine the number of active users on the same page and put it
    into the context
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'visitors_on_page usage: {% visitors_on_page as visitors %}')

    return VisitorsOnSite(varname, same_page=True)


register = template.Library()
register.tag(visitors_on_site)
register.tag(visitors_on_page)
