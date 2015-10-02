# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from comments.config import get_config
from comments.models import CustomComment
from comments.serializers import CommentDetailSerializer
from userspace.serializers import UserDetailSerializer
from .models import Marker, Vote


class MarkerSerializer(serializers.ModelSerializer):
    """ Serializer to use with map scripts.

    This serializer should be used only with ``list`` and ``retrieve`` methods.
    For other methods use ``MarkerSimpleSerializer`` which provides only
    basic fields to fill.

    The second thing to remember: this serializer uses methods related to
    active user, so it takes ``Context`` instance during initialization when
    we can pass ``auth.User`` instance to fetch user's votes.
    """
    content_type = serializers.SerializerMethodField('get_content_type')
    comment_count = serializers.SerializerMethodField('get_comment_count')
    comment_meta = serializers.SerializerMethodField('get_comment_meta')
    user_vote = serializers.SerializerMethodField('get_user_vote')
    voters = serializers.SerializerMethodField('get_voters')

    class Meta:
        model = Marker

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj).pk

    def get_comment_count(self, obj):
        return CustomComment.objects.for_model(obj).count()

    def get_voters(self, obj):
        voters = [x.user for x in obj.votes.all()]
        serializer = UserDetailSerializer(voters, many=True)
        return serializer.data

    def get_user_vote(self, obj):
        user = self.context['request'].user
        if user.is_anonymous() or not obj.votes.filter(user=user).count():
            return False
        return True

    def get_comment_meta(self, obj):
        qs = CustomComment.objects.for_model(obj).filter(parent__isnull=True)\
                                                     .order_by('-submit_date')
        return {
            'has_next': len(qs) > get_config('PAGINATE_BY'),
            'results': CommentDetailSerializer(qs[:get_config('PAGINATE_BY')],
                    many=True, context=self.context).data, }


class VoteSerializer(serializers.ModelSerializer):
    """ Serializes user vote to save in DB.
    """
    class Meta:
        model = Vote

