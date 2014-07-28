# -*- coding: utf-8 -*-
import json, datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.http import HttpResponse
from django.shortcuts import render
from .models import CustomComment, CommentVote


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
    ctx = []
    
    for comment in comments:
        ctx.append({
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
