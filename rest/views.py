# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest.serializers import *
from blog.models import News
from comments.models import CustomComment, CommentVote
from rest.permissions import IsOwnerOrReadOnly


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


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Intended to use with comment tree related to selected item
    """
    queryset = CustomComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        content_label = self.request.GET['content-label']
        content_type = ContentType.objects.get(pk=self.request.GET['content-type'])
        content_id = int(self.request.GET['content-id'])
        total_comments = CustomComment.objects.filter(content_type=content_type)
        total_comments = total_comments.filter(object_pk=content_id)
        return total_comments.order_by('-submit_date')

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.site_id = 1
        obj.object_pk = int(self.request.DATA['content_id'])
        obj.submit_date = timezone.now()
