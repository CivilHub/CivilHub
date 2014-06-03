# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from locations.models import Location
from ideas.models import Idea
from topics.models import Discussion
from blog.models import News


class LocationSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Location.objects.all()

    def lastmod(self, obj):
        return timezone.now()


class IdeaSitemap(Sitemap):
    changefreq = "daily"
    pririty = 0.5

    def items(self):
        return Idea.objects.all()


class DiscussionSitemap(Sitemap):
    changefreq = "hourly"
    pririty = 0.5

    def items(self):
        return Discussion.objects.all()


class NewsSitemap(Sitemap):
    changefreq = "always"
    pririty = 0.5

    def items(self):
        return News.objects.all()
