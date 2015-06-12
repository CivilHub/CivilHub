# -*- coding: utf-8 -*-
import collections
import datetime
import json

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.translation import ugettext as _

from actstream.models import Follow, target_stream

from locations.models import Location


class SetEncoder(json.JSONEncoder):
    """ Allows us to serialize python set as JSON.
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_ptr(val, total):
    """ Returns approximated percentage value given total and subset count.
    """
    return int(float(val)/float(total)*100)


def qs_by_time(qs, current):
    """ Filter action queryset on daily basis. Pass qs to filter and current
        time to compare to. It returns number or None if count is 0.
    """
    qs = qs.filter(timestamp__year=current.year,
                   timestamp__month=current.month,
                   timestamp__day=current.day).count()
    return qs if qs > 0 else None


def pie_chart(location):
    """ Pie chart presenting content type items published in selected location.
        Data is prepared to be presented as pie chart, with percentage values.
    """
    ideas = location.idea_set.count()
    polls = location.poll_set.count()
    news = location.news_set.count()
    discussions = location.discussion_set.count()
    projects = location.projects.count()
    total = sum([ideas, polls, discussions, projects, ])

    return json.dumps({
        'title': location.__unicode__(),
        'subtitle': _(u"Published content summary"),
        'name': _(u"Published items"),
        'series': {
            (_(u'ideas'), get_ptr(ideas, total), ),
            (_(u'polls'), get_ptr(polls, total), ),
            (_(u'news'), get_ptr(news, total), ),
            (_(u'discussions'), get_ptr(discussions, total), ),
            (_(u'projects'), get_ptr(projects, total), ),
        },
    }, cls=SetEncoder)


def summary_chart(location):
    return json.dumps({
        'title': location.__unicode__(),
        'subtitle': _(u"Published content summary"),
        'name': _(u"Published items"),
        'series': {
            (_(u'ideas'), location.idea_set.count(), ),
            (_(u'polls'), location.poll_set.count(), ),
            (_(u'news'), location.news_set.count(), ),
            (_(u'discussions'), location.discussion_set.count(), ),
            (_(u'projects'), location.projects.count(), ),
        },
    }, cls=SetEncoder)


def actions_chart(location):
    """ Summary of different kinds of actions related to particular location.
    """
    content_items = ['ideas', 'polls', 'news', 'discussions', 'projects', ]

    content_types = {
        'ideas': ContentType.objects.get(app_label='ideas', model='idea'),
        'polls': ContentType.objects.get(app_label='polls', model='poll'),
        'news': ContentType.objects.get(app_label='blog', model='news'),
        'discussions': ContentType.objects.get(app_label='topics', model='discussion'),
        'projects': ContentType.objects.get(app_label='projects', model='socialproject'),
    }

    stream = target_stream(location)

    started = stream.last().timestamp
    current = started
    maximum = timezone.now() + datetime.timedelta(hours=12)

    labels = {
        'ideas': _(u"ideas"),
        'polls': _(u"polls"),
        'news': _(u"news"),
        'discussions': _(u"discussions"),
        'projects': _(u"projects"),
    }

    counters = {
        'ideas': [],
        'polls': [],
        'news': [],
        'discussions': [],
        'projects': [],
    }

    while current < maximum:
        for itm in content_items:
            counters[itm].append(qs_by_time(stream.filter(
                action_object_content_type=content_types[itm]), current))
        current += datetime.timedelta(days=1)

    return json.dumps({
        'title': location.__unicode__(),
        'subtitle': _(u"Activity summary"),
        'started': str(started),
        'labels': labels,
        'series': counters, })


def follow_chart(location):
    """ Presents timeline data containing target location followers.
    """
    qs = Follow.objects.filter(object_id=location.pk,
            content_type=ContentType.objects.get_for_model(location))

    started = location.date_created
    current = started
    maximum = timezone.now() + datetime.timedelta(hours=12)
    prev_qs = 0

    followers = []
    while current < maximum:
        fqs = qs.filter(started__year=current.year,
                        started__month=current.month,
                        started__day=current.day).count()
        prev_qs += fqs
        followers.append(prev_qs)
        current += datetime.timedelta(days=1)

    return json.dumps({
        'title': location.__unicode__(),
        'subtitle': _(u"followers activity"),
        'name': _(u"followers"),
        'started': str(started),
        'series': followers, })
