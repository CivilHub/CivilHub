# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from taggit.models import Tag
from blog.models import Category, News
from ideas.models import Category as IdeaCategory
from ideas.models import Vote as IdeaVote
from comments.models import CustomComment, CommentVote
from topics.models import Category as ForumCategory
from topics.models import Discussion
from places_core.models import AbuseReport
from userspace.models import Badge
from gallery.models import LocationGalleryItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer to show short info during mouse hover
    """
    id = serializers.Field(source='pk')
    email = serializers.CharField()
    username = serializers.CharField()
    fullname = serializers.CharField(source='get_full_name')
    rank_pts = serializers.IntegerField(source='profile.rank_pts')
    avatar   = serializers.CharField(source='profile.avatar.url')
    follows  = serializers.Field(source='profile.get_biggest_locations')
    user_link= serializers.CharField(source='profile.get_absolute_url')

    class Meta:
        model = User
        fields = ('id', 'username', 'email','fullname', 'rank_pts', 'avatar',
                  'follows', 'user_link')


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
    user_id = serializers.Field(source='creator.pk')
    user_full_name = serializers.Field(source='creator.get_full_name')
    avatar = serializers.Field(source='creator.profile.avatar.url')
    location = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.RelatedField()
    category_url = serializers.SerializerMethodField('category_search_url')
    edited = serializers.BooleanField()
    tags = serializers.RelatedField(many=True)
    comment_count = serializers.SerializerMethodField('get_comment_count')

    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'content', 'date_created', 
                  'date_edited', 'username', 'user_id', 'avatar', 'location',
                  'category', 'category_url', 'edited', 'tags', 'comment_count',
                  'user_full_name',)

    def get_comment_count(self, obj):
        pk = obj.pk
        content_type = ContentType.objects.get_for_model(obj)
        comments = CustomComment.objects.filter(content_type=content_type)
        return len(comments.filter(object_pk=pk))

    def category_search_url(self, obj):
        return reverse('locations:category_search', kwargs={
            'slug'    : obj.location.slug,
            'app'     : 'blog',
            'model'   : 'news',
            'category': obj.category.pk
        })


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


class IdeaVoteCounterSerializer(serializers.ModelSerializer):
    """
    Get user profile link along with vote value (positive or negative).
    """
    id = serializers.Field(source='pk')
    username = serializers.Field(source='user.username')
    user_full_name = serializers.Field(source='user.get_full_name')
    user_avatar = serializers.Field(source='user.profile.avatar.url')
    vote = serializers.Field()

    class Meta:
        model = IdeaVote
        fields = ('id', 'username', 'user_full_name', 'user_avatar', 'vote',)


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


class BadgeSerializer(serializers.ModelSerializer):
    """
    Serializer class for user badges.
    """
    id   = serializers.Field(source='pk')
    name = serializers.CharField()
    description = serializers.CharField()
    thumbnail   = serializers.Field(source='thumbnail.url')

    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'thumbnail',)


class GalleryItemSerializer(serializers.ModelSerializer):
    """ Serializer class for location gallery items. """
    id = serializers.Field(source='pk')

    class Meta:
        model = LocationGalleryItem
