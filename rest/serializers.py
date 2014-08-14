# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.core.urlresolvers import reverse
from taggit.models import Tag
from blog.models import Category, News
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from ideas.models import Vote as IdeaVote
from comments.models import CustomComment, CommentVote
from topics.models import Category as ForumCategory
from topics.models import Discussion, Entry
from places_core.models import AbuseReport
from places_core.helpers import truncatehtml
from userspace.models import Badge
from gallery.models import LocationGalleryItem, UserGalleryItem
from locations.models import Location
from polls.models import Poll


class TranslatedModelSerializer(serializers.ModelSerializer):
    """
    Serializer dla obiektów przerobionych przez django-modeltranslation.
    """
    def __init__(self, *args, **kwargs):
        super(TranslatedModelSerializer, self).__init__(*args, **kwargs)
        ct = ContentType.objects.get_for_model(self.Meta.model)
        self.queryset = ct.get_all_objects_for_this_type()
        self.fields = self.get_fields()

    def get_fields(self):
        from rest_framework.fields import ModelField
        baned_idx = []
        fields = super(TranslatedModelSerializer, self).get_fields()
        for field, val in fields.iteritems():
            if not get_language().replace('-','_') in field and \
            isinstance(val, ModelField):
                baned_idx.append(field)
        for idx in baned_idx: del fields[idx]
        return fields


class MyActionsSerializer(serializers.Serializer):
    """
    Serializer for user activity stream.
    """
    id = serializers.Field(source='pk')
    verb = serializers.Field()
    timestamp = serializers.Field(source='timesince')
    actor = serializers.SerializerMethodField('get_actor_data')
    object = serializers.SerializerMethodField('get_action_object')
    object_ct = serializers.SerializerMethodField('get_verbose_name')
    target = serializers.SerializerMethodField('get_action_target')
    target_ct = serializers.Field(source='target_content_type.model')
    description = serializers.SerializerMethodField('get_action_description')

    def get_verbose_name(self, obj):
        try:
            ct = obj.action_object_content_type
            target = ct.get_object_for_this_type(pk=obj.action_object_object_id)
            return target._meta.verbose_name
        except Exception:
            return u''

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
            serializer = NewsBasicSerializer(instance)
            return serializer.data
        elif content_type.model == 'idea':
            serializer = IdeaBasicSerializer(instance)
            return serializer.data
        elif content_type.model == 'poll':
            serializer = PollBasicSerializer(instance)
            return serializer.data
        elif content_type.model == 'locationgalleryitem':
            serializer = GalleryItemSerializer(instance)
            return serializer.data
        elif content_type.model == 'discussion':
            serializer = DiscussionSerializer(instance)
            serializer.data['name'] = serializer.data['question']
            return serializer.data
        else:
            data = {
                'id': instance.pk,
                'url': self.get_object_url(obj),
            }
            return data

    def get_action_description(self, obj):
        try:
            ct = obj.action_object_content_type
            target = ct.get_object_for_this_type(pk=obj.action_object_object_id)
            if obj.verb == 'commented':
                return truncatehtml(obj.data['comment'], 140) + ' <a href="' + obj.data['comment_url'] + '">' + _("More") + '</a>'
            elif obj.verb == 'voted on':
                if obj.data['vote']:
                    return '<div class="vote-up"></div>'
                else:
                    return '<div class="vote-down"></div>'
                return obj.data['vote']
            elif ct.model == 'idea':
                return truncatehtml(target.description, 140)
            elif ct.model == 'location':
                return truncatehtml(target.description, 140)
            elif ct.model == 'news':
                return truncatehtml(target.content, 140)
            elif ct.model == 'poll':
                return truncatehtml(target.question, 140)
            elif ct.model == 'discussion':
                return truncatehtml(target.intro, 140)
            elif ct.model == 'entry':
                return truncatehtml(target.content, 140)
            elif ct.model == 'locationgalleryitem':
                return '<img src="' + target.get_thumbnail((128,128)) + '" />';
            else:
                return u''
        except Exception:
            return u''
        
    def get_action_object(self, obj):
        try:
            ct = obj.action_object_content_type
            target = ct.get_object_for_this_type(pk=obj.action_object_object_id)
            return self.serialize_selected_object(ct, target)
        except Exception:
            return {}
            
    def get_action_target(self, obj):
        try:
            ct = obj.target_content_type
            target = ct.get_object_for_this_type(pk=obj.target_object_id)
            return self.serialize_selected_object(ct, target)
        except Exception:
            return {}
    
    def get_actor_data(self, obj):
        """ WARNING: we assume that every actor is user instance!!!. """
        user = User.objects.get(pk=obj.actor_object_id)
        serializer = UserSerializer(user)
        return serializer.data


class PaginatedActionSerializer(PaginationSerializer):
    """ Paginate results for lazy loader. """
    class Meta:
        object_serializer_class = MyActionsSerializer


class BasicSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='pk')
    name = serializers.CharField(source='__unicode__')
    url = serializers.Field(source='get_absolute_url')
    
    class Meta:
        abstract = True

class LocationBasicSerializer(BasicSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'url',)

class IdeaBasicSerializer(BasicSerializer):
    class Meta:
        model = Idea
        fields = ('id', 'name', 'url',)

class NewsBasicSerializer(BasicSerializer):
    class Meta:
        model = News
        fields = ('id', 'name', 'url',)

class PollBasicSerializer(BasicSerializer):
    name = serializers.CharField(source='title')
    class Meta:
        model = Poll
        fields = ('id', 'name', 'url',)


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
    follows  = serializers.SerializerMethodField('get_followed_locations')
    #follows  = serializers.Field(source='profile.get_biggest_locations')
    user_link= serializers.CharField(source='profile.get_absolute_url')

    class Meta:
        model = User
        fields = ('id', 'username', 'email','fullname', 'rank_pts', 'avatar',
                  'follows', 'user_link')

    def get_followed_locations(self, obj):
        locations = obj.profile.get_biggest_locations()
        serializer = LocationBasicSerializer(locations, many=True)
        return serializer.data


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


class NewsSimpleSerializer(serializers.ModelSerializer):
    """
    Serializer przeznaczony dla API mobilnej aplikacji. Uproszczony POST itp.
    """
    slug = serializers.SlugField(required=False)
    creator = serializers.PrimaryKeyRelatedField(required=False)

    class Meta:
        model = News


class NewsSerializer(serializers.ModelSerializer):
    """
    News serializer - API endpoint for news Backbone application.
    """
    id = serializers.Field(source='pk')
    title = serializers.CharField(max_length=64)
    slug = serializers.SlugField(required=False)
    link = serializers.Field(source='get_absolute_url')
    content = serializers.Field(source='get_entry_introtext')
    date_created = serializers.DateTimeField(required=False)
    date_edited = serializers.DateTimeField(required=False)
    username = serializers.Field(source='creator.username')
    user_id = serializers.Field(source='creator.pk')
    user_full_name = serializers.Field(source='creator.get_full_name')
    avatar = serializers.Field(source='creator.profile.avatar.url')
    creator_url = serializers.Field(source='creator.profile.get_absolute_url')
    location = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.RelatedField()
    category_url = serializers.SerializerMethodField('category_search_url')
    edited = serializers.BooleanField()
    tags = serializers.SerializerMethodField('get_tags')
    comment_count = serializers.SerializerMethodField('get_comment_count')
    comment_meta = serializers.SerializerMethodField('get_comment_meta')
    
    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'link', 'content', 'date_created', 
                  'date_edited', 'username', 'user_id', 'avatar', 'location',
                  'category', 'category_url', 'edited', 'tags', 'comment_count',
                  'user_full_name', 'creator_url', 'comment_meta')

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':obj.location.slug,
                                       'tag':tag.name})
            })
        return tags

    def get_comment_meta(self, obj):
        return {
            'content-type': ContentType.objects.get_for_model(News).pk,
            'content-label': 'blog',
        }

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


class PollSerializer(serializers.ModelSerializer):
    """ Standard poll serializer. """
    id = serializers.Field(source='pk')
    title = serializers.CharField()
    question = serializers.CharField()
    url = serializers.Field(source='get_absolute_url')
    creator_id = serializers.Field(source='creator.pk')
    creator_username = serializers.Field(source='creator.username')
    creator_fullname = serializers.Field(source='creator.get_full_name')
    creator_url = serializers.Field(source='creator.profile.get_absolute_url')
    creator_avatar = serializers.Field(source='creator.profile.avatar.url')
    date_created = serializers.DateTimeField()
    tags = serializers.SerializerMethodField('get_tags')
    answers_url = serializers.SerializerMethodField('get_answers_url')

    class Meta:
        model = Poll
        fields = ('id', 'title', 'question', 'url', 'creator_id', 'creator_username',
                  'creator_fullname', 'creator_url', 'creator_avatar', 'date_created',
                  'tags', 'answers_url',)

    def get_answers_url(self, obj):
        return reverse('polls:results', kwargs={'pk': obj.pk})

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':obj.location.slug,
                                       'tag':tag.name})
            })
        return tags


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

    def get_contenttype(self, obj):
        return ContentType.objects.get_for_model(CustomComment).pk


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
    id = serializers.Field(source='pk')
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


class DiscussionSerializer(serializers.ModelSerializer):
    """ Basic serializer for discussions. """
    id = serializers.Field(source='pk')
    question = serializers.CharField()
    intro = serializers.CharField()
    location = serializers.PrimaryKeyRelatedField()
    url = serializers.Field(source='get_absolute_url')
    creator_id = serializers.Field(source='creator.pk')
    creator_username = serializers.Field(source='creator.username')
    creator_fullname = serializers.Field(source='creator.get_full_name')
    creator_url = serializers.Field(source='creator.profile.get_absolute_url')
    creator_avatar = serializers.Field(source='creator.profile.avatar.url')
    date_created = serializers.DateTimeField(required=False)
    date_edited = serializers.DateTimeField(required=False)
    status = serializers.BooleanField()
    category_name = serializers.Field(source='category.name')
    category_url = serializers.SerializerMethodField('category_search_url')
    tags = serializers.SerializerMethodField('get_tags')
    answers = serializers.SerializerMethodField('get_answer_count')

    class Meta:
        model = Discussion
        fields = ('id', 'question', 'intro', 'url', 'creator_id', 'answers',
                  'creator_fullname', 'creator_url', 'creator_avatar', 'category_name',
                  'date_created', 'date_edited', 'status', 'category_url', 'tags',
                  'creator_username', 'location',)

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':obj.location.slug,
                                       'tag':tag.name})
            })
        return tags

    def category_search_url(self, obj):
        return reverse('locations:category_search', kwargs={
            'slug'    : obj.location.slug,
            'app'     : 'topics',
            'model'   : 'discussion',
            'category': obj.category.pk
        })

    def get_answer_count(self, obj):
        return obj.entry_set.count()


class DiscussionReplySerializer(serializers.ModelSerializer):
    """ 
    This is serializer to use in dynamically created list under
    discussion - e.g. list of other user's replies. 
    """
    id = serializers.Field(source='pk')
    content = serializers.CharField()
    creator_id = serializers.Field(source='creator.pk')
    creator_username = serializers.Field(source='creator.username')
    creator_fullname = serializers.Field(source='creator.get_full_name')
    creator_avatar = serializers.Field(source='creator.profile.avatar.url')
    creator_url = serializers.Field(source='creator.profile.get_absolute_url')
    date_created = serializers.DateTimeField(required=False)
    date_edited = serializers.DateTimeField(required=False)
    is_edited = serializers.BooleanField()
    vote_count = serializers.Field(source='votes.count')

    class Meta:
        model = Entry
        fields = ('id', 'content', 'creator_id', 'creator_username', 'creator_fullname',
                  'creator_avatar', 'date_created', 'date_edited', 'is_edited',
                  'creator_url', 'vote_count',)


class IdeaCategorySerializer(serializers.ModelSerializer):
    """
    Allow superusers to create new idea categories dynamically.
    """
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = IdeaCategory
        fields = ('name', 'description',)


class IdeaSerializer(serializers.ModelSerializer):
    """ Idea serializer. """
    id = serializers.Field(source='pk')
    name = serializers.CharField()
    url = serializers.Field(source='get_absolute_url')
    description = serializers.CharField()
    creator_id = serializers.Field(source='creator.pk')
    creator_url = serializers.Field(source='creator.profile.get_absolute_url')
    creator_username = serializers.Field(source='creator.username')
    creator_fullname = serializers.Field(source='creator.get_full_name')
    creator_avatar = serializers.Field(source='creator.profile.avatar.url')
    date_created = serializers.DateTimeField(required=False)
    date_edited = serializers.DateTimeField(required=False)
    category_name = serializers.SerializerMethodField('get_category_name')
    category_url = serializers.SerializerMethodField('category_search_url')
    total_comments = serializers.Field(source='get_comment_count')
    total_votes = serializers.Field(source='get_votes')
    edited = serializers.BooleanField()
    tags = serializers.SerializerMethodField('get_tags')
    comment_meta = serializers.SerializerMethodField('get_comment_meta')

    class Meta:
        model = Idea
        fields = ('id','name','description','creator_id','creator_username',
                 'creator_fullname','creator_avatar','date_created','date_edited',
                 'edited','tags','category_name','category_url','total_comments',
                 'total_votes','url','creator_url', 'comment_meta',)

    def get_comment_meta(self, obj):
        return {
            'content-type': ContentType.objects.get_for_model(Idea).pk,
            'content-label': 'ideas',
        }

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':obj.location.slug,
                                       'tag':tag.name})
            })
        return tags

    def category_search_url(self, obj):
        if obj.category:
            return reverse('locations:category_search', kwargs={
                'slug'    : obj.location.slug,
                'app'     : 'topics',
                'model'   : 'discussion',
                'category': obj.category.pk
            })
        return r''

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return u''


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
    object_pk     = serializers.IntegerField()
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
    name = serializers.CharField()
    description = serializers.CharField()
    thumbnail = serializers.SerializerMethodField('item_thumbnail')
    picture = serializers.Field(source='url')
    url = serializers.Field(source='get_absolute_url')
    comment_meta = serializers.SerializerMethodField('get_comment_meta')

    def get_comment_meta(self, obj):
        return {
            'content-type': ContentType.objects.get_for_model(LocationGalleryItem).pk,
            'content-label': 'gallery',
        }

    def item_thumbnail(self, obj):
        return obj.get_thumbnail((128,128))

    class Meta:
        model = LocationGalleryItem
        fields = ('id', 'comment_meta', 'description', 'thumbnail', 'picture',
                  'name', 'url',)


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
