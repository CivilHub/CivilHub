# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag
from blog.models import Category, News
from ideas.models import Category as IdeaCategory
from comments.models import CustomComment, CommentVote
from topics.models import Category as ForumCategory
from topics.models import Discussion
from places_core.models import AbuseReport


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
    pk = serializers.Field(source='pk')
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class NewsSerializer(serializers.ModelSerializer):
    """
    News serializer - API endpoint for news Backbone application.
    """
    id = serializers.Field(source='pk')
    title = serializers.CharField(max_length=64)
    slug = serializers.SlugField()
    content = serializers.Field(source='get_entry_introtext')
    date_created = serializers.DateTimeField()
    date_edited = serializers.DateTimeField()
    username = serializers.Field(source='creator.username')
    user_full_name = serializers.Field(source='creator.get_full_name')
    avatar = serializers.Field(source='creator.profile.avatar.url')
    location = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.RelatedField()
    tags = serializers.RelatedField(many=True)
    comment_count = serializers.SerializerMethodField('get_comment_count')

    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'content', 'date_created', 
                  'date_edited', 'username', 'avatar', 'location', 'category',
                  'tags', 'comment_count', 'user_full_name',)

    def get_comment_count(self, obj):
        pk = obj.pk
        content_type = ContentType.objects.get_for_model(obj)
        comments = CustomComment.objects.filter(content_type=content_type)
        return len(comments.filter(object_pk=pk))


class CommentSerializer(serializers.ModelSerializer):
    """
    Custom comments
    """
    id = serializers.Field()
    comment = serializers.CharField(max_length=1024)
    submit_date = serializers.DateTimeField(required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.Field(source='user.username')
    user_full_name = serializers.Field(source='user.get_full_name')
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
                  'total_votes', 'upvotes', 'downvotes', 'user_full_name',)


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


class ForumCategorySerializer(serializers.ModelSerializer):
    """
    Allow superusers to create new forum categories dynamically.
    """
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = ForumCategory
        fields = ('name', 'description',)


class IdeaCategorySerializer(serializers.ModelSerializer):
    """
    Allow superusers to create new idea categories dynamically.
    """
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = IdeaCategory
        fields = ('name', 'description',)


class AbuseReportSerializer(serializers.ModelSerializer):
    """
    Abuse reports to send in context of some content.
    """
    id = serializers.Field()
    comment = serializers.CharField(max_length=2048)
    sender  = serializers.PrimaryKeyRelatedField(read_only=True)
    status  = serializers.Field()
    content_type  = serializers.PrimaryKeyRelatedField()
    object_pk     = serializers.RelatedField()
    date_reported = serializers.DateTimeField(required=False)

    class Meta:
        model = AbuseReport
        fields = ('id', 'comment', 'sender', 'status', 'content_type',
               'object_pk', 'date_reported',)
