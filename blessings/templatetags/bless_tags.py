# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Library

from ..models import Blessing

register = Library()


@register.simple_tag(takes_context=True)
def blessbox(context, obj):
    context.update({
        'pk': obj.pk,
        'ct': ContentType.objects.get_for_model(obj).pk, })
    blessings = Blessing.objects.for_model(obj)
    if len(blessings):
        context.update({
            'item_counter': len(blessings),
            'last_user': blessings.first().user,
            'count_others': blessings.count() - 1, })
    if len(blessings.filter(user=context['request'].user)):
        context.update({'user_vote': True, })
    template = loader.get_template('blessings/blessbox.html')
    return template.render(context)
