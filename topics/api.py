# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions

from rest.permissions import IsOwnerOrReadOnly, \
                             IsModeratorOrReadOnly, \
                             IsSuperuserOrReadOnly

from .models import Category, Discussion, Entry
from .serializers import ForumCategorySimpleSerializer, \
                        ForumTopicSimpleSerializer, \
                        ForumEntrySimpleSerializer, \
                        ForumCategorySerializer


class ForumCategoryAPIViewSet(viewsets.ModelViewSet):
    """ Forum categories. """
    queryset = Category.objects.all()
    paginate_by = None
    serializer_class = ForumCategorySerializer
    permission_classes = (IsSuperuserOrReadOnly,)


class ForumTopicAPIViewSet(viewsets.ModelViewSet):
    """
    This is simplified discussion view set for mobile app.
    """
    queryset = Discussion.objects.all()
    serializer_class = ForumTopicSimpleSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.creator = self.request.user


class ForumEntryAPIViewSet(viewsets.ModelViewSet):
    """
    Simple view to manage topic answers.
    """
    queryset = Entry.objects.all()
    serializer_class = ForumEntrySimpleSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        discussion_id = self.request.QUERY_PARAMS.get('pk', None)
        if discussion_id:
            discussion = get_object_or_404(Discussion, pk=discussion_id)
            return Entry.objects.filter(discussion=discussion)
        return super(ForumEntryAPIViewSet, self).get_queryset()

    def pre_save(self, obj):
        obj.creator = self.request.user