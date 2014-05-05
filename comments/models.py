# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from userspace.models import UserProfile


class CustomComment(MPTTModel, Comment):
    """
    Basic comment model extending mptt model so it could be nested
    """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['submit_date']

    def get_reply_comments(self):
        return len(CustomComment.objects.filter(parent=self))

class CommentVote(models.Model):
    """
    Users can vote up or down on comments, but only once
    """
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)
    comment = models.ForeignKey(CustomComment, related_name='comments')
    date_voted = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.vote

    def is_valid_vote(username):
        user = User.objects.get(username=username)
        return len(self.objects.filter(user=user)) <= 0
