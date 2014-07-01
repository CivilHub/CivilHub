# -*- coding: utf-8 -*-
import json, math
from operator import itemgetter
from taggit.models import Tag
from locations.models import Location


def truncatesmart(value, limit=40):
    """
    Truncates a string after a given number of chars keeping whole words.
    """
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    value = unicode(value)
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    # Cut the string
    value = value[:limit]
    
    # Break into words and remove the last
    words = value.split(' ')[:-1]
    
    # Join the words and return
    return ' '.join(words) + '...'


class SimplePaginator(object):
    """
    Prosty paginator wyników zapytań prezentowanych w formie JSON. Ta klasa
    została stworzona z myślą o wykorzystaniu w widokach nie serwowanych
    przez Django REST Server.
    It takes 2 mandatory parameters - queryset to filter and total number of 
    items to display per one page.
    """
    queryset = None
    per_page = 0
    length   = 0

    def __init__(self, queryset, per_page):
        self.queryset = queryset
        self.per_page = per_page
        self.length = int(math.ceil(len(self.queryset)/(self.per_page*1.0)))

    def count(self):
        return self.length

    def page(self, page):
        """ Get single results page. """
        set_finish = int(page) * self.per_page
        return self.queryset[set_finish-self.per_page:set_finish]


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
