# -*- coding: utf-8 -*-
import re
import urlparse

from django import  forms
from django.db import models
from django.utils.translation import ugettext_lazy as _


def validate_youtube_url(value):
    pattern = r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$'

    if value[:16] == 'http://youtu.be/':
        if re.match(r'\w+', value[16:]) is None:
            raise forms.ValidationError(_('Not a valid Youtube URL'))
    elif re.match(pattern, value) is None:
        raise forms.ValidationError(_('Not a valid Youtube URL'))


class YoutubeUrl(unicode):
    @property
    def video_id(self):
        parsed_url = urlparse.urlparse(self)
        if parsed_url.query == '':
            return parsed_url.path
        return urlparse.parse_qs(parsed_url.query)['v'][0]

    @property
    def embed_url(self):
        return 'https://youtube.com/embed/%s/' % self.video_id

    @property
    def thumb(self):
        return "https://img.youtube.com/vi/%s/2.jpg" % self.video_id


class YoutubeUrlField(models.URLField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(YoutubeUrlField, self).__init__(*args, **kwargs)
        self.validators.append(validate_youtube_url)

    def to_python(self, value):

        url = super(YoutubeUrlField, self).to_python(value)

        return YoutubeUrl(url)

    def get_prep_value(self, value):
        return unicode(value)
