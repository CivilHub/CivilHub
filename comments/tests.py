# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from locations.models import Location
from ideas.models import Idea

from .models import CustomComment, CommentVote


class CommentVotesTestCase(TestCase):
    """ """
    fixtures = ['fixtures/users.json',]

    def setUp(self):
        self.testuser = User.objects.create(username='testuser')
        self.user = User.objects.first()
        self.location = Location.objects.create(
            name="testplace",
            creator=self.user,
            kind='country',
            country_code='PL'
        )
        self.idea = Idea.objects.create(
            name="Test Idea",
            description="Test Idea",
            creator=self.user,
            location=self.location
        )

    def test_comment_vote_unicode(self):
        """ See: https://app.getsentry.com/civilhuborg/civilhub/group/59274298/ """
        comment = CustomComment.objects.create(
            content_type = ContentType.objects.get_for_model(Idea),
            object_pk = self.idea.pk,
            user = self.testuser,
            comment = "This is test comment",
            submit_date = timezone.now(),
            site_id = 1
        )
        vote = CommentVote.objects.create(user=self.user, comment=comment, vote=True)
        self.assertIsInstance(vote.__str__(), str)
