# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest.serializers import *
from blog.models import News

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
