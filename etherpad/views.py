# -*- coding: utf-8 -*-
import datetime
import json
import time
import urllib

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView

from places_core.mixins import LoginRequiredMixin

from .client import EtherpadException, EtherpadLiteClient
from .forms import ServePadForm, PadCreationForm
from .models import EtherpadAuthor, Pad

SESS_LENGTH = 1 * 24 * 60 * 60
if hasattr(settings, 'ETHERPAD_SESSION_LENGTH'):
    SESS_LENGTH = settings.ETHERPAD_SESSION_LENGTH


class PadListView(ListView):
    """ List all pads in database or just those related to selected group. """
    model = Pad
    paginate_by = 25

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        if group_id is not None:
            return self.model.objects.filter(group__id=group_id)
        return super(PadListView, self).get_queryset()


class PadExternalView(DetailView):
    """ This view is intended for visitors without direct access to pad's
    content. Page presents pad's content converted to HTML format. """
    model = Pad

    def get_context_data(self, object=None):
        context = super(PadExternalView, self).get_context_data()
        context['download_form'] = ServePadForm(initial={
            'pad': self.get_object(),
            'format': '.txt',
        })
        return context


class EtherPadEditView(LoginRequiredMixin, DetailView):
    """ This is view that allows users with pad access to edit it's content. """
    model = Pad
    template_name = 'etherpad/pad_content.html'

    def get_context_data(self, **kwargs):
        context = super(EtherPadEditView, self).get_context_data(**kwargs)
        context['pad_url'] = '{}/p/{}${}'.format(
            settings.ETHERPAD_EXTERNAL_URL,
            self.object.group.etherpad_id,
            urllib.quote(self.object.name.encode('utf-8'), '_'))
        return context

    def render_to_response(self, context, **response_kwargs):
        try:
            author = EtherpadAuthor.objects.get(user=self.request.user)
        except EtherpadAuthor.DoesNotExist:
            author = None
        if author is None or not self.object.group in author.group.all():
            raise PermissionDenied
        response = super(EtherPadEditView, self).render_to_response(context, **response_kwargs)
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=SESS_LENGTH)
        client = EtherpadLiteClient(
            base_params={'apikey': settings.ETHERPAD_API_KEY},
            base_url=settings.ETHERPAD_INTERNAL_URL)
        result = client.createSession(
            groupID=self.object.group.etherpad_id,
            authorID=author.etherpad_id,
            validUntil=time.mktime(expires.timetuple()).__str__())
        # Delete the existing session first (if there is any)
        if ('padSessionID' and 'sessionID' in self.request.COOKIES):
            try:
                client.deleteSession(sessionID=self.request.COOKIES['sessionID'])
            except EtherpadException:
                pass
            response.delete_cookie('sessionID')
            response.delete_cookie('padSessionID')
        # Set the new session cookie for both the server and the local site
        # This will not work if etherpad-lite is running on external host.
        # TODO: we probably should set cookie for server.external_url
        response.set_cookie('sessionID', value=result['sessionID'],
                            expires=expires, httponly=False)
        response.set_cookie('padSessionID', value=result['sessionID'],
                            expires=expires, httponly=False)
        return response


class ServePadView(FormView):
    """ Visitors should be able to download pad in selected format. without
    AbiWord installed on system, the only available format is .txt. """
    form_class = ServePadForm
    template_name = 'etherpad/download_form.html'

    def get_initial(self):
        initial = super(ServePadView, self).get_initial()
        pad_pk = self.kwargs.get('pk')
        if pad_pk is not None:
            initial['pad'] = get_object_or_404(Pad, pk=pad_pk)
        return initial

    def form_valid(self, form):
        """ TODO: for now we serve only .txt files. More formats required! """
        pad = form.cleaned_data['pad']
        response = HttpResponse(pad.text, content_type='text/plain')
        response['Content-Disposition'] = "attachment; filename=%s.txt" % pad.pad_id
        return response


class DeletePadView(LoginRequiredMixin, DeleteView):
    """ In this view users can delete their pads. """
    model = Pad

    def get_success_url(self):
        group = self.object.group
        if group.socialproject_set.count():
            slug = group.socialproject_set.first().slug
            return reverse('projects:documents', kwargs={'slug': slug})
        return '/'

    def delete(self, *args, **kwargs):
        group = self.get_object().group
        author = EtherpadAuthor.objects.get(user=self.request.user)
        if not group in author.group.all():
            raise PermissionDenied
        return super(DeletePadView, self).delete(*args, **kwargs)


class CreatePadView(LoginRequiredMixin, CreateView):
    """ In this view authorized users may create new pads for groups to which they belong. """
    model = Pad
    form_class = PadCreationForm

    def get_success_url(self):
        return reverse('pad-collaborate', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        if self.request.is_ajax():
            context = {
                'success': False,
                'errors': form.errors,
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        return super(CreatePadView, self).form_invalid()

    def form_valid(self, form):
        group = form.cleaned_data.get('group')
        author = EtherpadAuthor.objects.get(user=self.request.user)
        if not group in author.group.all():
            raise PermissionDenied
        return super(CreatePadView, self).form_valid(form)


class UpdatePadView(LoginRequiredMixin, UpdateView):
    """ This view allows authorized users to change pad's settings. """
    model = Pad

    def form_valid(self, form):
        group = form.cleaned_data.get('group')
        author = EtherpadAuthor.objects.get(user=self.request.user)
        if not group in author.group.all():
            raise PermissionDenied
        return super(UpdatePadView, self).form_valid(form)
