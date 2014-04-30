# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest.serializers import *
from blog.models import News
from comments.models import CustomComment, CommentVote

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class NewsViewSet(viewsets.ViewSet):
    """
    API endpoint that allows news to be viewed or edited.
    """
    queryset = News.objects.all()
    def list(self, request):
        queryset = News.objects.all()
        serializer = NewsSerializer
        return Response(serializer.data)
        
class CommentsViewSet(viewsets.ViewSet):
    """
    Intended to use with comment tree related to selected item
    """
    queryset = CustomComment.objects.all()
    def list(self, request):
        queryset = CustomComment.objects.all()
        serializer = CommentSerializer
        return Response(serializer.data)
