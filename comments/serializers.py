# -*- coding: utf-8 -*-
import json

from django.core import serializers as dj_serializers

from rest_framework import serializers

from userspace.serializers import UserDetailSerializer

from .models import CustomComment, CommentVote


class CustomCommentSerializer(serializers.ModelSerializer):
    """
    This is basic serializer for comment model. It will simplify CRUD operations.
    """

    class Meta:
        model = CustomComment


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    This is serializer meant to be read-only. It presents detailed info about
    comment to be displayed in some front-end template.
    """
    author = serializers.SerializerMethodField('get_user_data')
    content_object = serializers.SerializerMethodField('get_content_object')
    upvotes = serializers.Field(source='upvotes')
    downvotes = serializers.Field(source='downvotes')
    note = serializers.Field(source='note')
    answers = serializers.SerializerMethodField('get_answer_count')
    permission = serializers.SerializerMethodField('check_permission')
    reason = serializers.Field(source='get_reason_display')

    def get_user_data(self, obj):
        serializer = UserDetailSerializer(obj.user)
        return serializer.data

    def get_content_object(self, obj):
        if obj.content_object is None:
            return None
        data = dj_serializers.serialize("json", [obj.content_object, ])
        return json.loads(data)[0]

    def get_answer_count(self, obj):
        return obj.children.count()

    def check_permission(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated():
            return obj.has_permission(request.user)
        return False

    class Meta:
        model = CustomComment
        fields = ('id', 'content_type', 'object_pk', 'submit_date', 'comment',
                  'parent', 'author', 'content_object', 'upvotes', 'downvotes',
                  'note', 'answers', 'permission', 'is_removed', 'reason', )


class CommentVoteSerializer(serializers.ModelSerializer):
    """
    This serializer is very simple, it will help us combine front-end scripts
    to allow registered users to vote for other's comments.
    """

    class Meta:
        model = CommentVote
