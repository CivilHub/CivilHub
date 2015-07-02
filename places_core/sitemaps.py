# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from civmaps import Sitemap
from locations.models import Location
from ideas.models import Idea
from topics.models import Discussion
from blog.models import News
from polls.models import Poll
from etherpad.models import Pad
from projects.models import SocialProject
from articles.models import Article


class LocationSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Location.objects.all()

    def lastmod(self, obj):
        return timezone.now()


class IdeaSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Idea.objects.all()

    def lastmod(self, obj):
        return obj.date_edited


class DiscussionSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Discussion.objects.all()


class NewsSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return News.objects.all()


class PollsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Poll.objects.all()


class ProjectsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return SocialProject.objects.all()


class ArticleSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Article.objects.all()


class EtherpadSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Pad.objects.all()


from organizations.models import Organization
class OrganizationSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Organization.objects.all()


from guides.models import Guide
class GuideSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Guide.objects.all()
