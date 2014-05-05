# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Category, News
from comments.models import CustomComment, CommentVote


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer to show short info during mouse hover
    """
    class Meta:
        model = User
        fields = ('username', 'email')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Category serializer - quickly add and manage categories
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """
    Custom comments
    """
    id = serializers.Field()
    comment = serializers.CharField(max_length=1024)
    submit_date = serializers.DateTimeField(required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.Field(source='user.username')
    avatar = serializers.Field(source='user.profile.avatar.url')
    content_type = serializers.PrimaryKeyRelatedField()
    object_pk = serializers.Field()
    replies = serializers.Field(source='get_reply_comments')

    class Meta:
        model = CustomComment
        fields = ('id', 'comment', 'submit_date', 'user', 'parent', 'username',
                  'avatar', 'content_type', 'object_pk', 'replies')
