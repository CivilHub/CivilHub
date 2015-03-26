# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from haystack import indexes
from locations.models import Location
from topics.models import Discussion
from blog.models import News
from ideas.models import Idea
from polls.models import Poll


class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Localization search engine.
    """
    text = indexes.EdgeNgramField(document=True)
    name = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Location

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class DiscussionIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Title search engine forum.
    """
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='question')
    intro = indexes.CharField(model_attr='intro')
    location = indexes.IntegerField(model_attr='location__pk')

    def get_model(self):
        return Discussion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    """
    News search engine.
    """
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class IdeasIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Idea search engine.
    """
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Idea

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PollsIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Poll search engine.
    """
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr='title')
    question = indexes.CharField(model_attr='question')

    def get_model(self):
        return Poll

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class UserSearchIndex(indexes.SearchIndex, indexes.Indexable):
    """
    User search engine by user name / name / surname.
    """
    text = indexes.CharField(document=True)
    username = indexes.CharField(model_attr='username')
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    email = indexes.CharField(model_attr='email')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
