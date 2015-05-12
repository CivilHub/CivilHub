# -*- coding: utf-8 -*-
import json

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView

from locations.helpers import get_followers_from_location
from places_core.mixins import LoginRequiredMixin

from civmail import messages as mails
from .forms import ContactForm, FollowersEmailForm


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
        return render(request, self.template_name,
                      {'title': _("Invite people")})

    def post(self, request):
        """ Send emails. """
        emails = request.POST.get('emails').split(',')
        user_url = request.build_absolute_uri(
            request.user.profile.get_absolute_url())
        user_profile_img = request.build_absolute_uri(
            request.user.profile.avatar.url)
        message = {
            'link': {
                'name': request.POST.get('name'),
                'href': request.POST.get('link'),
            },
            'user_link': user_url,
            'user_name': request.user.get_full_name(),
            'user_img': user_profile_img,
            'lang': translation.get_language_from_request(request),
        }
        for address in emails:
            address = address.strip()
            try:
                email = mails.InviteToContentMail()
                email.send(address, message)
            except:
                # FIXME: Not valid email. Should be cleaned up in form
                pass
        if request.is_ajax():
            context = {
                'success': True,
                'message': self.success_message,
                'level': 'success',
            }
            return HttpResponse(json.dumps(context),
                                content_type="application/json")
        messages.add_message(request, messages.SUCCESS, self.success_message)
        return redirect('/invite-friends/')


class ComposeFollowersMessage(LoginRequiredMixin, FormView):
    """
    View for form that allows superusers and administrators to send email
    messages to all of selected location's (and it's children) followers.
    This functionality is available only for superusers.
    """
    template_name = 'civmail/followers_form.html'
    form_class = FollowersEmailForm
    success_url = '/activity/'
    success_message = _(u"All messages sent successfully")

    def get_initial(self):
        initial = super(ComposeFollowersMessage, self).get_initial()
        initial['location_id'] = self.kwargs.get('pk')
        return initial

    def get(self, request, pk=None):
        if not request.user.is_superuser:
            raise Http404
        return super(ComposeFollowersMessage, self).get(request)

    def post(self, request, pk=None):
        if not request.user.is_superuser:
            raise Http404
        return super(ComposeFollowersMessage, self).post(request)

    def form_valid(self, form):
        followers = get_followers_from_location(
            form.cleaned_data['location_id'],
            deep=True)
        for user in followers:
            email_context = {
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
                'lang': user.profile.lang,
            }
            message = mails.FollowersNotificationMesage()
            message.send(user.email, email_context)
        messages.add_message(self.request, messages.SUCCESS,
                             self.success_message)
        return super(ComposeFollowersMessage, self).form_valid(form)


class ContactEmailView(FormView):
    """
    """
    template_name = 'civmail/contact_form.html'
    form_class = ContactForm

    def get_form_kwargs(self):
        kwargs = super(ContactEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, _("Message sent"))
        return redirect(reverse('contact'))
