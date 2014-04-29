# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Category, News

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
        fields = ('name', 'description')
        
class NewsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Add news to location news list
    """
    class Meta:
        model = News
        fields = ('title', 'content', 'location', 'creator', 'categories', 'date_created')
