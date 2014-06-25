# -*- conding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils import translation
from django.utils.translation import ugettext as _
from places_core.mixins import LoginRequiredMixin
from civmail import messages as mails


class InviteToContentView(LoginRequiredMixin, View):
    """
    This view is bind with modal window form allowing registered users to send
    messages with invitation to currently selected content. In practice that
    means we send current page url along with page's title, assuming that it
    is closely bind to content.
    """
    http_method_names = [u'get', u'post']
    template_name = 'civmail/invite-users.html'

    def get(self, request):
        """ Show modal form. """
        return render(request, self.template_name, {'title':_("Invite people")})

    def post(self, request):
        """ Send emails. """
        emails = request.POST.get('emails').split(',')
        translation.activate(request.user.profile.lang)
        message = {
            'link': {
                'name': request.POST.get('name'),
                'href': request.POST.get('link'),
            },
            'inviting_user': request.user
        }
        for address in emails:
            address = address.strip()
            try:
                email = mails.InviteToContentMail()
                email.send(address, message)
            except:
                print address, "is not valid email."
        context = {
            'success': True,
            'message': _("All messages sent successfully"),
            'level'  : 'success',
        }
        return HttpResponse(json.dumps(context))
