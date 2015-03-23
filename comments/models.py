# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey

from places_core.helpers import sanitizeHtml


class CustomComment(MPTTModel, Comment):
    """
    Basic comment model extending mptt model so it could be nested
    """
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['submit_date']

    def save(self, *args, **kwargs):
        self.comment = sanitizeHtml(self.comment)
        super(CustomComment, self).save(*args, **kwargs)

    def get_reply_comments(self):
        return len(CustomComment.objects.filter(parent=self))

    def get_upvotes(self):
        return len(self.votes.filter(vote=True))

    def get_downvotes(self):
        return len(self.votes.filter(vote=False))

    def calculate_votes(self):
        votes_total = self.votes
        votes_up = len(votes_total.filter(vote=True))
        votes_down = len(votes_total.filter(vote=False))
        return votes_up - votes_down

    def get_absolute_url(self):
        """
        Fake this function to redirect to parent object and get rid
        of actstream error.
        """
        return self.content_object.get_absolute_url()


@python_2_unicode_compatible
class CommentVote(models.Model):
    """
    Users can vote up or down on comments, but only once
    """
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)
    comment = models.ForeignKey(CustomComment, related_name='votes')
    date_voted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vote
