# -*- coding: utf-8 -*-
import json, datetime

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from rest_framework.renderers import JSONRenderer

from .models import CustomComment, CommentVote
from .serializers import CommentDetailSerializer


def get_related_comments(object_id, app_label, model_label):
    """
    Get related comments for given object
    """
    model = get_model(app_label=app_label, model_name=model_label)
    content_type = ContentType.objects.get_for_model(model)

    comments = CustomComment.objects.filter(content_type=content_type).filter(object_pk=int(object_id))

    return comments


def get_comment_count(request, object_id, app_label, model_label):
    """
    Get number of comments for selected target
    """
    comments = get_related_comments(object_id, app_label, model_label)

    ctx = {
        'success': True,
        'message': len(comments),
    }

    return HttpResponse(json.dumps(ctx));


def get_comment_votes(comment):
    """
    Get total votes on this comment
    """
    total_votes = CommentVote.objects.filter(idea=comment)
    votes_up = len(total_votes.filter(vote=True))
    votes_down = len(total_votes.filter(vote=False))

    return votes_up - votes_down


def get_comment_tree(request, object_id, app_label, model_label):
    """
    Get complete comment tree for designated target
    """
    comments = get_related_comments(object_id, app_label, model_label)
    ctx = {'results': []}
    paginator = Paginator(comments, setting.PAGE_PAGINATION_LIMIT)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    ctx['next'] = str(int(page)+1) if page < paginator.num_pages else None
    ctx['prev'] = str(int(page)-1) if page > 1 else None

    for comment in comments:
        ctx['results'].append({
            'comment': comment.comment,
            'submit_date': comment.submit_date.strftime('%Y-%m-%d %H:%M'),
            'author': comment.user.username,
            'author_name': comment.user_name,
            'author_email': comment.user_email,
            'author_url': comment.user_url,
            'is_public': comment.is_public,
            'is_removed': comment.is_removed,
            'votes': get_comment_votes(comment),
        })

    return HttpResponse(json.dumps(ctx))


class CommentSummaryView(ListView):
    """ Static view with list of all comments related to selected object.
    """
    model = CustomComment

    def dispatch(self, *args, **kwargs):
        try:
            ct = kwargs.get('content_ct')
            pk = kwargs.get('content_pk')
        except (TypeError, ValueError, ):
            raise Http404
        self.content_type = get_object_or_404(ContentType, pk=ct)
        self.content_object = self.content_type.get_object_for_this_type(pk=pk)
        return super(CommentSummaryView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(CommentSummaryView, self).get_queryset()
        return qs.filter(content_type=self.content_type,
                         object_pk=self.content_object.pk,
                         parent__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(CommentSummaryView, self).get_context_data(**kwargs)
        serializer = CommentDetailSerializer(self.get_queryset(), many=True)
        data = json.loads(JSONRenderer().render(serializer.data))
        data = {
            'has_next': False,
            'results': json.loads(JSONRenderer().render(serializer.data)), }
        context.update({
            'ct': self.content_type.pk,
            'content_type': self.content_object._meta.model_name,
            'object_id': self.content_object.pk,
            'content_object': self.content_object,
            'object_count': len(data['results']),
            'object_list': json.dumps(data), })
        return context
