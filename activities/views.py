# -*- coding: utf-8 -*-
import json
import urllib
import urllib2

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from actstream.models import following
from social.apps.django_app.default.models import UserSocialAuth

from userspace.models import UserProfile


class CivilUserMixin(SingleObjectMixin):
    """ Provides common context for user activities views.
    """
    model = UserProfile
    slug_field = "clean_username"
    slug_url_kwarg = "username"
    context_object_name = "profile"
    template_name = "activities/followed_user_list.html"

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(CivilUserMixin, self).dispatch(*args, **kwargs)


class FollowedUserList(CivilUserMixin, View):
    """ Presents list of all users followed by given user.
    """
    def get_context_data(self):
        context = super(FollowedUserList, self).get_context_data()
        context.update({
            'object_list': [x for x in following(self.object.user, User)\
                                                    if x is not None], })
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class FacebookFriendList(CivilUserMixin, View):
    """ List of all facebook friends of currently logged in user.
    """
    def get_context_data(self):
        url = 'https://graph.facebook.com/{}/friends?{}'
        params = urllib.urlencode({
            'access_token': self.s_auth.extra_data['access_token'],
            'fields': ['id', ], })
        res = urllib2.urlopen(url.format(self.s_auth.extra_data['id'], params))
        id_list = [x['id'] for x in json.loads(res.read())['data']]
        context = super(FacebookFriendList, self).get_context_data()
        fb_users = UserSocialAuth.objects.filter(provider='facebook')
        friends = [x.user for x in fb_users if x.extra_data['id'] in id_list]
        context.update({'object_list': friends, 'fb_list': True, })
        return context

    def get(self, request, **kwargs):
        user = self.request.user
        if user.is_anonymous() or user != self.object.user:
            raise Http404
        try:
            self.s_auth = self.object.user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            request.session['relogin'] = json.dumps({
                'backend': 'facebook',
                'next_url': request.path, })
            return render(request, 'userspace/fb-login-required.html', {
                'profile': self.request.user.profile, })
        return render(request, self.template_name, self.get_context_data())
