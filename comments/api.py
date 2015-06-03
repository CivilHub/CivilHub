# -*- coding: utf-8 -*-
from django.db.models import Count
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework import viewsets, permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework.views import APIView

from userspace.serializers import UserDetailSerializer

from .models import CustomComment, CommentVote
from .serializers import CustomCommentSerializer, CommentDetailSerializer


class CommentList(viewsets.ModelViewSet):
    """
    This is main comment view set. It is meant to present list of comments.
    By default all comments will be shown, but we may pass `ct` and `pk` as
    query params (content type id and object id, respectively) to fetch only
    comments related to given object. In this situation only first-level
    comments will be returned, eg:

        /api-comments/list/?ct=43&pk=1

    It is also possible to get next-level replies for selected comment. In this
    case we have to pass query param `parent` with selected comment ID, eg:

        /api-comments/list/?parent=25

    The last thing are filters. We can pass `o` parameter with one of this values:

    <dl>
        <dt><code>new</code></dt>
        <dd>List items from newest to oldest</dd>

        <dt><code>old</code></dt>
        <dd>List items from oldest to newest</dd>

        <dt><code>votes</code></dt>
        <dd>List by total votes count (both negative and positive)</dd>
    </dl>

    Default ordering is the same as with `new` option.
    """
    model = CustomComment
    paginate_by = 5
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        qs = super(CommentList, self).get_queryset()
        ct = self.request.QUERY_PARAMS.get('ct')
        pk = self.request.QUERY_PARAMS.get('pk')
        parent = self.request.QUERY_PARAMS.get('parent')
        if ct is not None and pk is not None:
            qs = qs.filter(content_type__id=ct,
                           object_pk=pk,
                           parent__isnull=True)
        elif parent is not None:
            qs = qs.filter(parent__id=parent)
        order = self.request.QUERY_PARAMS.get('o')
        if order == 'old':
            return qs.order_by('submit_date')
        elif order == 'votes':
            qs = qs.annotate(num_votes=Count('votes'))
            return qs.order_by('-num_votes', '-submit_date')
        return qs.order_by('-submit_date')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CommentDetailSerializer
        else:
            return CustomCommentSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.submit_date = timezone.now()

    @action()
    def vote(self, request, pk):
        vote = request.DATA.get('vote')
        comment = self.get_object()
        cv, created = CommentVote.objects.get_or_create(
            user=request.user,
            comment=comment,
            vote=True
        )
        context = {'created': created, 'id': cv.pk}
        if created:
            context.update({
                'status': 'success',
                'message': _(u"Vote saved"),
            })
        else:
            context.update({
                'status': 'warning',
                'message': _(u"You have already voted for this comment"),
            })
        return Response(context)

    @link()
    def summary(self, request, pk):
        comment = self.get_object()
        v_filter = request.QUERY_PARAMS.get('v', 'all')
        if v_filter == 'up':
            votes = comment.votes.filter(vote=True)
        elif v_filter == 'down':
            votes = comment.votes.filter(vote=False)
        else:
            votes = comment.votes.all()
        users = [x.user for x in votes]
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)


class CommentAnswers(APIView):
    """
    Here we can get answers for specific comments. Just pass `pk` as query
    parameter to get all next-level responses for comment with this id.
    """
    model = CustomComment

    def get(self, request):
        pk = request.QUERY_PARAMS.get('pk')
        if pk is None:
            raise Http404
        qs = self.model.objects.filter(parent__id=pk)
        serializer = CommentDetailSerializer(qs, many=True)
        return Response(serializer.data)
