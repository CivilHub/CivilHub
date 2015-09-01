# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import serializers, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest.permissions import IsOwnerOrReadOnly

from .models import Idea, Vote
from .serializers import IdeaSimpleSerializer, \
                         IdeaDetailSerializer, \
                         VoteDetailSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    """ Main viewset for Idea objects. Regular GET request will return list.
    Additional paths:

    vote
    ----
    <p>Only POST requests. `vote` parameter is required in any case.</p>
    <p>There are three possible values - 1 (positive), 2 (negative 3 (revoked).
    We cannot delete vote from database, so we have to change it's state to
    3 in this case. Such votes will be ignored on any other list.</p>
    <p>Second parameter is `comment`, which is required only for negative
    votes.</p>
    <p>Example:</p>
    <pre class="prettyprint">var data = {csrfmiddlewaretoken: "the_token", vote: 1};
    $.post('/api-ideas/ideas/43/vote/', data, function (r) {
      console.log(r);
    });</pre>

    votes
    -----
    <p>Only GET requests. Detailed vote summary for single Idea.</p>
    <p>Example:</p>
    <pre class="prettyprint">$.get('/api-ideas/ideas/596/votes/', function (r) {
      console.log(r);
    });</pre>
    """
    model = Idea
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return IdeaDetailSerializer
        else:
            return IdeaSimpleSerializer

    @action()
    def vote(self, request, pk):
        vote = request.DATA.get('vote')
        comment = request.DATA.get('comment')
        user = request.user
        if user.is_anonymous():
            raise PermissionDenied
        idea = self.get_object()

        results = idea.vote(user, vote, comment)

        results['message'] = _(u"Your vote has been revoked")

        if results.get('prev_target') == 1:
            label = _(u"Vote YES")
        elif results.get('prev_target') == 2:
            label = _(u"Report critical remark")
        else:
            label = _(u"Revoke")
            results['message'] = _(u"Your vote has been saved")
        results['label'] = label

        if results.get('is_reversed'):
            results['new_label'] = results['label']
            results['label'] = _(u"Revoke")

        return Response({'result': results, })

    @link()
    def votes(self, request, pk):
        votes = self.get_object().vote_set.exclude(status=3)
        return Response(VoteDetailSerializer(votes, many=True).data)


class IdeaVoteViewSet(viewsets.ReadOnlyModelViewSet):
    model = Vote
    serializer_class = VoteDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        try:
            idea_id = int(self.request.QUERY_PARAMS.get('i'))
            return Vote.objects.filter(idea=get_object_or_404(Idea, pk=idea_id))
        except (TypeError, ValueError, ):
            return Vote.objects.all()
