# -*- coding: utf-8 -*-
import datetime

from rest_framework import serializers

from django.utils import timezone

from userspace.serializers import UserDetailSerializer

from .models import Answer, AnswerSet, Poll


class AnswerSerializer(serializers.ModelSerializer):
    """ Used by other serializers to hold answer data.
    """
    class Meta:
        model = Answer
        fields = ('id', 'answer', )


class AnswerSetBasicSerializer(serializers.ModelSerializer):
    """ Used by other serializers to hold answer data.
    """
    class Meta:
        model = AnswerSet
        fields = ('id', 'user', 'answers', 'date', )


class AnswerSetSerializer(serializers.ModelSerializer):
    """ The most important serializer for basic graphs - formatting answers.
    """
    answers = serializers.SerializerMethodField('get_answers')

    def get_answers(self, obj):
        answers = {}
        for a in obj.answer_set.all():
            count = obj.answerset_set.filter(
                answers__in=[a.pk, ]).values('pk').count()
            if obj.multiple:
                answers[a.answer] = count
            else:
                answers[a.answer] = int(
                    float(count)/float(obj.answerset_set.count())*100)
        return answers

    class Meta:
        model = Poll
        fields = ('id', 'title', 'multiple', 'answers', )


class TimelineSetSerializer(serializers.ModelSerializer):
    """ Used by timeline graphs - presents list of all answers.
    """
    labels = serializers.SerializerMethodField('get_labels')
    answers = serializers.SerializerMethodField('get_answers')

    def get_labels(self, obj):
        return [{'id': x[0], 'label': x[1], } for x in \
                obj.answer_set.values_list('pk', 'answer')]

    def get_answers(self, obj):
        the_time = obj.date_created
        stop_time = timezone.now()
        labels = self.get_labels(obj)

        answers = {}
        for label in labels:
            answers[label['id']] = []

        while the_time < stop_time:
            for label in labels:
                qs = obj.answerset_set.filter(answers__in=[label['id'], ],
                                              date__year=the_time.year,
                                              date__month=the_time.month,
                                              date__day=the_time.day)
                answers[label['id']].append(qs.values('pk').count())
            the_time = the_time + datetime.timedelta(days=1)

        return answers

    class Meta:
        model = Poll
        fields = ('title', 'question', 'date_created', 'labels', 'answers', )
