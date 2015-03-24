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
    fixtures = ['fixtures/users.json',
                'fixtures/locations.json',
                'fixtures/ideas.json',]

    def setUp(self):
        u = User.objects.get(username='jakub_pocentek')
        l = Location.objects.get(slug="brzeg-pl-1")
        i = Idea.objects.create(name="Test Idea", description="Test Idea", creator=u, location=l)
        c = CustomComment.objects.create(
            content_type = ContentType.objects.get_for_model(Idea),
            object_pk = i.pk,
            user = User.objects.get(username="wujek_fester"),
            comment = "This is test comment",
            submit_date = timezone.now(),
            site_id = 1
        )
        self.vote = CommentVote.objects.create(user=u, comment=c, vote=True)

    def test_comment_vote_unicode(self):
        """ See: https://app.getsentry.com/civilhuborg/civilhub/group/59274298/ """
        self.assertIsInstance(self.vote.__str__(), str)
