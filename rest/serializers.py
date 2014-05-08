# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from taggit.models import Tag
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


class NewsSerializer(serializers.ModelSerializer):
    """
    News serializer - API endpoint for news Backbone application.
    """
    id = serializers.Field(source='pk')
    title = serializers.CharField(max_length=64)
    content = serializers.CharField(max_length=10248)
    date_created = serializers.DateTimeField()
    date_edited = serializers.DateTimeField()
    username = serializers.Field(source='creator.username')
    avatar = serializers.Field(source='creator.profile.avatar.url')

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'date_created', 'date_edited',
                  'username', 'avatar', )


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
    total_votes = serializers.Field(source='calculate_votes')
    upvotes = serializers.Field(source='get_upvotes')
    downvotes = serializers.Field(source='get_downvotes')

    class Meta:
        model = CustomComment
        fields = ('id', 'comment', 'submit_date', 'user', 'parent', 'username',
                  'avatar', 'content_type', 'object_pk', 'replies',
                  'total_votes', 'upvotes', 'downvotes')


class CommentVoteSerializer(serializers.ModelSerializer):
    """
    Votes for comments send via AJAX.
    Fields marked as required=False are validated elsewhere.
    """
    pk = serializers.Field()
    vote = serializers.CharField(default="up")
    comment = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = CommentVote
        fields = ('pk', 'vote', 'comment')


class TagSerializer(serializers.ModelSerializer):
    """
    Allow fetching existing tags for jQuery Autocomplete.
    """
    label = serializers.CharField(source='name')

    class Meta:
        model = Tag
        fields = ('label',)
