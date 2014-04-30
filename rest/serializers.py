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
        
class NewsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Add news to location news list
    """
    class Meta:
        model = News
        fields = ('id')
        
class CommentSerializer(serializers.Serializer):
    """
    Custom comments
    """
    comment = serializers.CharField(max_length=1024)
        
    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.comment = attrs.get('comment', instance.comment)
            return instance

        # Create new instance
        return CustomComment(**attrs)
