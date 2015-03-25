# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.utils import translation
from django.utils.translation import ugettext as _

from places_core.mixins import LoginRequiredMixin
from civmail import messages as mails


class InviteFriendsView(LoginRequiredMixin, TemplateView):
    """ View allows you to invite your friends. """
    template_name = 'civmail/invite-friends.html'


class InviteToContentView(LoginRequiredMixin, View):
    """
    This view is bind with modal window form allowing registered users to send
    messages with invitation to currently selected content. In practice that
    means we send current page url along with page's title, assuming that it
    is closely bind to content.
    """
    http_method_names = [u'get', u'post']
    template_name = 'civmail/invite-users.html'
    success_message = _(u"All messages sent successfully")

    def get(self, request):
        """ Show modal form. """
        return render(request, self.template_name, {'title':_("Invite people")})

    def post(self, request):
        """ Send emails. """
        emails = request.POST.get('emails').split(',')
        translation.activate(request.user.profile.lang)
        user_url = request.build_absolute_uri(request.user.profile.get_absolute_url())
        message = {
            'link': {
                'name': request.POST.get('name'),
                'href': request.POST.get('link'),
            },
            'user_link': user_url,
            'user_name': request.user.get_full_name()
        }
        for address in emails:
            address = address.strip()
            try:
                email = mails.InviteToContentMail()
                email.send(address, message)
            except:
                print address, "is not valid email."
        if request.is_ajax():
            context = {
                'success': True,
                'message': self.success_message,
                'level'  : 'success',
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        messages.add_message(request, messages.SUCCESS, self.success_message)
        return redirect('/invite-friends/')
