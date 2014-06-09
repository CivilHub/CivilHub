# -*- coding: utf-8 -*-
import json
from operator import itemgetter
from taggit.models import Tag
from locations.models import Location

class TagFilter(object):
    """
    Custom class to filter tags related only to items in selected
    location.
    """
    location  = None # selected location
    _tag_list = {}   # tag.name > tag.count dictionary


    def __init__(self, location):
        """ Get all tagged objects and prepare tag list. """
        self.location = location
        news_list = self.location.news_set.all()
        idea_list = self.location.idea_set.all()
        poll_list = self.location.poll_set.all()
        self._filter_tags(news_list, idea_list, poll_list)


    def _filter_tags(self, *args):
        """ Prepare dict containing tags in location and their counter. """
        # reset tags to avoid displaying double numbers after page refresh.
        self._tag_list = {}
        itemlist = []
        for arg in args:
            itemlist += arg
        for itm in itemlist:
            for tag in itm.tags.all():
                if tag.name and len(tag.name) > 0:
                    try:
                        self._tag_list[tag.name] += 1
                    except KeyError:
                        self._tag_list[tag.name] = 1


    def get_tags(self, format=None, order=None):
        """ Returns tag list in few formats and different order. """
        tags = self._tag_list
        if order == 'count':
            tags = sorted(tags.items(), key=itemgetter(1))
        if format == 'json':
            return json.dumps(tags)
        else:
            return tags.iteritems()


    def count_tags(self, tag):
        """ Count how many times given tag was used. """
        try:
            return self._tag_list[tag]
        except KeyError:
            return 0
