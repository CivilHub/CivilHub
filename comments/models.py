# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from notifications.models import notify
from places_core.config import ABUSE_REASONS
from places_core.helpers import sanitizeHtml
from places_core.permissions import is_moderator

from .helpers import notify_author


class CustomComment(MPTTModel, Comment):
    """
    Basic comment model extending mptt model so it could be nested.
    """
    REASONS = ABUSE_REASONS

    parent = TreeForeignKey('self', null=True, blank=True,
                                    related_name='children')
    reason = models.PositiveIntegerField(choices=REASONS, default=6,
                                         verbose_name=_(u"reason"))

    @property
    def upvotes(self):
        return len(self.votes.filter(vote=True))

    @property
    def downvotes(self):
        return len(self.votes.filter(vote=False))

    @property
    def note(self):
        return self.upvotes - self.downvotes

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
        if self.content_object is not None:
            content_type = ContentType.objects.get_for_model(self.content_object)
            the_url = self.content_object.get_absolute_url()
            return '{}#content-{}'.format(the_url, self.pk)
        return ""

    def has_permission(self, user):
        """ Check if given user is permitted to moderate this comment.
        """
        if user.is_superuser:
            return True
        if self.content_object is not None:
            if hasattr(self.content_object, 'location'):
                return is_moderator(user, self.content_object.location)
        return False

    def toggle(self, vote=None):
        """ Mark comment to be hidden instead of displayed entirely.
        """
        if not self.is_removed:
            self.is_removed = True
        else:
            self.is_removed = False
        if vote is not None:
            self.reason = vote
        self.save()
        if self.is_removed:
            notify_author(self)
        return self.is_removed

    class MPTTMeta:
        order_insertion_by = ['submit_date']

    class Meta:
        verbose_name = _(u"comment")
        verbose_name_plural = _(u"comments")


@python_2_unicode_compatible
class CommentVote(models.Model):
    """
    Users can vote up or down on comments, but only once.
    """
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)
    comment = models.ForeignKey(CustomComment, related_name='votes')
    date_voted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u"comment vote")
        verbose_name_plural = _(u"comment votes")
        unique_together = ('user', 'comment', )

    def __str__(self):
        msg = 'negatively'
        if self.vote:
            msg = 'positively'
        return u"{} voted {} for {}".format(self.user.get_full_name(), msg,
                                            self.comment)


def comment_notification(sender, instance, created, **kwargs):
    """
    Send notification for commented object creator. Handles special case of
    task participants, when we want to notify them all at once.
    """
    if not created or instance.parent is not None:
        # this is edited comment or answer for other comment
        # They have their own hooks in places_core.actions.
        return True
    if instance.content_object.__class__.__name__ == 'Task':
        # Special case - send notifications to all task participants
        for user in instance.content_object.participants.exclude(
            pk=instance.user.pk):
            notify(instance.user, user,
                key="comment",
                verb=_(u"commented task"),
                action_object=instance,
                action_target=instance.content_object)

    # Get target user to notify depending on commented object's type.
    target_user = None
    if hasattr(instance.content_object, 'creator'):
        # Regular content objects usually have 'creator' field
        target_user = instance.content_object.creator
    elif hasattr(instance.content_object, 'author'):
        # Projects and some other models that use other convention
        target_user = instance.content_object.author

    # Notify users only when someone else commented their objects.
    if target_user is not None and instance.user != target_user:
        notify(instance.user, target_user,
            key="customcomment",
            verb="commented your",
            action_object=instance,
            action_target=instance.content_object)


models.signals.post_save.connect(comment_notification, sender=CustomComment)
