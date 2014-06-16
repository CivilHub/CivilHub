# -*- coding: utf-8 -*-
import json
from operator import itemgetter
from taggit.models import Tag
from locations.models import Location


class ContentFilter(object):
    """
    Custom class to filter tags related only to items in selected location.
    """
    news_list = []
    idea_list = []
    poll_list = []

    def __init__(self, location):
        """ Prepare object list. """
        self.location = location
        self._items = {}
        self.news_list = self.location.news_set.all()
        self.idea_list = self.location.idea_set.all()
        self.poll_list = self.location.poll_set.all()

    def get_items(self, format=None, order=None):
        """ Returns items in few formats and different order. """
        items = self._items
        if order == 'count':
            items = sorted(items.items(), key=itemgetter(1))
        if format == 'json':
            return json.dumps(items)
        else:
            return items.iteritems()

    def count_items(self, itm):
        """ Count how many times given item was used. """
        try:
            return self._items[itm]
        except KeyError:
            return 0


class TagFilter(ContentFilter):
    """
    Custom class to filter tags related only to items in selected
    location.
    """
    def __init__(self, location):
        """ Get all tagged objects and prepare tag list. """
        super(TagFilter, self).__init__(location)
        self._filter_tags(self.news_list, self.idea_list, self.poll_list)


    def _filter_tags(self, *args):
        """ Prepare dict containing tags in location and their counter. """
        itemlist = []
        for arg in args:
            itemlist += arg
        for itm in itemlist:
            for tag in itm.tags.all():
                if tag.name and len(tag.name) > 0:
                    try:
                        self._items[tag.name] += 1
                    except KeyError:
                        self._items[tag.name] = 1
