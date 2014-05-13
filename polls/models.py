from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from locations.models import Location
from taggit.managers import TaggableManager


class Category(models.Model):
    """
    Categories for polls - their not mandatory, but we allow users to choose
    or add some to create some hierarchy.
    """
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Poll(models.Model):
    """
    Base poll class - means entire poll.
    """
    title = models.CharField(max_length=128)
    tags  = TaggableManager()
    creator  = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'),
                                        null=True, blank=True,)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    description   = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class Question(models.Model):
    """
    Single question model.
    """
    question  = models.CharField(max_length=256)
    poll      = models.ForeignKey(Poll)
    help_text = models.CharField(max_length=256)
    multiple  = models.BooleanField(default=False)

    def get_correct_answer(self):
        return self.answer_set.filter(correct=True)

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    """
    Single answer model.
    """
    answer = models.CharField(max_length=256)
    question = models.ForeignKey(Question)
    correct  = models.BooleanField(default=False)

    def __unicode__(self):
        return self.answer
