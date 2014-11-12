# -*- coding: utf-8 -*-
import json, math, os, re, icu
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup, Comment
from uuid import uuid4 as uuid
from PIL import Image
from operator import itemgetter
from taggit.models import Tag
from django.conf import settings
from django.core.files import File

tag_end_re = re.compile(r'(\w+)[^>]*>')
entity_end_re = re.compile(r'(\w+;)')


def sanitizeHtml(value, base_url=None):
    """
    Allow only whitelisted tags. I have changed this method slightly to allow
    defining tag whitelist in project's settings module.
    
    @see: http://stackoverflow.com/questions/16861/sanitising-user-input-using-python/25136#25136
    """
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    validTags = settings.VALID_TAGS
    validAttrs = settings.VALID_ATTRS
    urlAttrs = settings.URL_ATTRS
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        # Get rid of comments
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in validTags:
            tag.hidden = True
        attrs = tag.attrs
        tag.attrs = []
        for attr, val in attrs:
            if attr in validAttrs:
                val = re_scripts.sub('', val) # Remove scripts (vbs & js)
                if attr in urlAttrs:
                    val = urljoin(base_url, val) # Calculate the absolute url
                tag.attrs.append((attr, val))

    return soup.renderContents().decode('utf8')


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


def truncatehtml(string, length, ellipsis='...'):
    """Truncate HTML string, preserving tag structure and character entities."""
    length = int(length)
    output_length = 0
    i = 0
    pending_close_tags = {}
    
    while output_length < length and i < len(string):
        c = string[i]

        if c == '<':
            # probably some kind of tag
            if i in pending_close_tags:
                # just pop and skip if it's closing tag we already knew about
                i += len(pending_close_tags.pop(i))
            else:
                # else maybe add tag
                i += 1
                match = tag_end_re.match(string[i:])
                if match:
                    tag = match.groups()[0]
                    i += match.end()
  
                    # save the end tag for possible later use if there is one
                    match = re.search(r'(</' + tag + '[^>]*>)', string[i:], re.IGNORECASE)
                    if match:
                        pending_close_tags[i + match.start()] = match.groups()[0]
                else:
                    output_length += 1 # some kind of garbage, but count it in
                    
        elif c == '&':
            # possible character entity, we need to skip it
            i += 1
            match = entity_end_re.match(string[i:])
            if match:
                i += match.end()

            # this is either a weird character or just '&', both count as 1
            output_length += 1
        else:
            # plain old characters
            
            skip_to = string.find('<', i, i + length)
            if skip_to == -1:
                skip_to = string.find('&', i, i + length)
            if skip_to == -1:
                skip_to = i + length
                
            # clamp
            delta = min(skip_to - i,
                        length - output_length,
                        len(string) - i)

            output_length += delta
            i += delta
                        
    output = [string[:i]]
    if output_length == length:
        output.append(ellipsis)

    for k in sorted(pending_close_tags.keys()):
        output.append(pending_close_tags[k])

    return "".join(output)


def sort_by_locale(queryset, key, language):
    """
    Prosta funkcja, która korzysta z biblioteki PyICU do sortowania wyników
    wyszukiwania alfabetycznie z uwzględnieniem znaków UTF konkretnego języka.
    
    Parametr `queryset` jest wymagany, może to być zarówno Django queryset jak
    i zwykła pythonowa lista.
    
    Parametr `key` to funkcja, wq której będziemy sortować. 
    
    Parametr language również jest wymagany. To kod języka w standardzie ISO
    (pl, en etc.) podany jako string.
    """
    code = language.lower() + '_' + language.upper() + '.' + 'UTF-8'
    collator = icu.Collator.createInstance(icu.Locale(code))
    q = list(queryset)
    q.sort(key=key, cmp=collator.compare)
    return q


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

    def page(self, page=None):
        """ Get single results page. """
        if not page: page = 1
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


def process_background_image(imgfile, dirname=None):
    """
    Scales image. This images are then used as background for location and 
    profile pages. 
    
    Function takes image file (usually from request.FILES['file']) as argument
    and changes it's size and name. If `dirname` is provided as path relative
    to MEDIA_ROOT settings, image will be saved on this path. If not ,`img`
    folder will be used instead.
    """
    img = Image.open(imgfile)
    pathname = dirname or 'img'
    dirname = os.path.join(settings.MEDIA_ROOT, pathname)
    imgname = str(uuid()) + str(len(os.listdir(dirname))) + '.jpg'
    if img.size[0] > settings.BACKGROUND_IMAGE_SIZE:
        img.thumbnail((settings.BACKGROUND_IMAGE_SIZE, settings.BACKGROUND_IMAGE_SIZE))
    img.save(os.path.join(dirname, imgname), 'JPEG')
    return File(open(os.path.join(dirname, imgname)))
