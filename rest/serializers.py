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
from gallery.models import LocationGalleryItem, UserGalleryItem
from locations.models import Location


class MyActionsSerializer(serializers.Serializer):
    """
    Serializer for user activity stream.
    """
    id = serializers.Field(source='pk')
    verb = serializers.Field()
    date_created = serializers.Field(source='timesince')
    actor = serializers.SerializerMethodField('get_actor_data')
    object = serializers.SerializerMethodField('get_action_object')
    object_ct = serializers.Field(source='action_object_content_type.model')
    target = serializers.SerializerMethodField('get_action_target')
    target_ct = serializers.Field(source='target_content_type.model')

    def get_object_url(self, obj):
        try:
            ct = obj.action_object_content_type
            target = ct.get_object_for_this_type(pk=obj.action_object_object_id)
            return target.get_absolute_url()
        except Exception:
            return u''

    def serialize_selected_object(self, content_type, instance):
        """ 
        Factory method to get serialized data for passed objects. It use's
        basic serializers if possible.
        """
        if content_type.model == 'location':
            serializer = LocationBasicSerializer(instance)
            return serializer.data
        elif content_type.model == 'news':
            serializer = NewsSerializer(instance)
            return serializer.data
        elif content_type.model == 'idea':
            serializer = IdeaBasicSerializer(instance)
            return serializer.data
        else:
            data = {
                'id': instance.pk,
                'url': self.get_object_url(obj),
            }
            return data
        
    def get_action_object(self, obj):
        try:
            ct = obj.action_object_content_type
            target = ct.get_object_for_this_type(pk=obj.action_object_object_id)
            return self.serialize_selected_object(ct, target)
        except Exception:
            return None
            
    def get_action_target(self, obj):
        try:
            ct = obj.target_content_type
            target = ct.get_object_for_this_type(pk=obj.target_object_id)
            return self.serialize_selected_object(ct, target)
        except Exception:
            return None
    
    def get_actor_data(self, obj):
        """ WARNING: we assume that every actor is user instance!!!. """
        user = User.objects.get(pk=obj.actor_object_id)
        serializer = UserSerializer(user)
        return serializer.data


class LocationBasicSerializer(serializers.ModelSerializer):
    """ Basic location serializer for lists etc. """
    id = serializers.Field(source='pk')
    name = serializers.CharField()
    url = serializers.Field(source='get_absolute_url')
    
    class Meta:
        model = Location
        fields = ('id', 'name', 'url')


class IdeaBasicSerializer(serializers.ModelSerializer):
    """ Serialize ideas in format appropriate for lists etc. """
    id = serializers.Field(source='pk')
    name = serializers.CharField()
    url = serializers.Field(source='get_absolute_url')
    
    class Meta:
        model = Location
        fields = ('id', 'name', 'url')


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
    user_url = serializers.Field(source='user.profile.get_absolute_url')
    user_full_name = serializers.Field(source='user.get_full_name')
    user_avatar = serializers.Field(source='user.profile.thumbnail.url')
    vote = serializers.Field()

    class Meta:
        model = IdeaVote
        fields = ('id', 'username', 'user_url', 'user_full_name',
                  'user_avatar', 'vote',)


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


class UserMediaSerializer(serializers.ModelSerializer):
    """ Serializer for items in user gallery. """
    id = serializers.Field(source='pk')
    picture_name = serializers.CharField()
    picture_url = serializers.Field(source='url')
    thumbnail = serializers.SerializerMethodField('get_thumbnail')

    def get_thumbnail(self, obj):
        return obj.get_thumbnail((128,128))

    class Meta:
        model = UserGalleryItem
        fields = ('id', 'picture_name', 'picture_url', 'thumbnail')
