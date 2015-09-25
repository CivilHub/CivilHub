# -*- coding: utf-8 -*-
import json

from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework import mixins, status, permissions, viewsets
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework.views import APIView

from userspace.serializers import UserDetailSerializer

from .models import CustomComment, CommentVote
from .serializers import CustomCommentSerializer, CommentDetailSerializer


class CommentUpdateModelMixin(mixins.UpdateModelMixin):
    """ This is modified mixin that allows us to perform PATCH request but
        returns detailed serializer. Should be very easy to use it anywhere
        else, for now, comment serializer is hardcoded.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object_or_none()

        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.pre_save(serializer.object)
        except ValidationError as err:
            # full_clean on model instance may be called in pre_save,
            # so we have to handle eventual errors.
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)

        if self.object is None:
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.object = serializer.save(force_update=True)
        self.post_save(self.object, created=False)
        s = CommentDetailSerializer(self.object)
        return Response(s.data, status=status.HTTP_200_OK)


class CommentList(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   CommentUpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
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

    Voting
    ------
    <p>Send simple POST request with `vote` parameter set to `true` or `false`.
    </p>
    <p>Example:</p>
    <pre class="prettyprint">var data = {csrfmiddlewaretoken: "the_token", vote: false};
    $.post('/api-comments/list/638/vote/', data, function (r) {
      console.log(r);
    });</pre>

    Creating comments
    -----------------
    Comments are tightly related to object's Content Type. You have to pass:<br>
    `comment` - Comment's content<br>
    `object_pk` - Commented object ID<br>
    `content_type` - Target Content Type ID (e.g. Idea, News, etc. but we have
    to pass numeric ID.<br>
    `submit_date` - Usually current timestamp, in standard ISO with TZ.<br>
    `site` - Legacy requirement. Just always pass `1` here.
    <p>Example:</p>
    <pre class="prettyprint">var data = {
      scrfmiddlewaretoken: "the_token",
      comment: "This is awesome comment!",
      object_pk: 1,
      content_type: 59,
      submit_date: '2015-09-01T12:44:20+02:00',
      site: 1
    };
    $.post('/api-comments/list/', data, function (r) {
      console.log(r);
    });</pre>

    Answers
    -------
    To create answer simply create new comment and add `parent` with commented
    comment (^-^) ID.
    """
    model = CustomComment
    paginate_by = 5
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

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
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            return CustomCommentSerializer
        else:
            return CommentDetailSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.submit_date = timezone.now()

    def pre_delete(self, obj):
        if self.request.user != obj.user:
            raise PermissionDenied

    def patch(self, request, *args, **kwargs):
        #return self.update_partial(request, *args, **kwargs)
        return Response("Test")

    @action()
    def vote(self, request, pk):
        vote = json.loads(request.DATA.get('vote'))
        comment = self.get_object()
        cv, created = CommentVote.objects.get_or_create(
            user=request.user,
            comment=comment,
            vote=vote)
        context = {'created': created, 'id': cv.pk, }
        if created:
            context.update({
                'status': 'success',
                'message': _(u"Vote saved"), })
        else:
            context.update({
                'status': 'warning',
                'message': _(u"You have already voted for this comment"), })
        return Response(context)

    @action()
    def moderate(self, request, pk):
        comment = self.get_object()
        try:
            vote = int(request.DATA.get('vote'))
        except (TypeError, ValueError, ):
            vote = None
        if not comment.has_permission(self.request.user):
            raise PermissionDenied
        if comment.toggle(vote=vote):
            message = _(u"Coment has been hidden")
        else:
            message = _(u"Coment has been restored")
        return Response({
            'is_removed': comment.is_removed,
            'message': message,
            'reason': comment.get_reason_display(), })

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
