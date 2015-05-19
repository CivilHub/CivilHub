# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator

from ..forms import AttachmentUploadForm
from ..models import Attachment, SocialProject
from ..permissions import check_access


def get_attachment(request, pk):
    """ We assume that everyone may download file.
    """
    attachment = get_object_or_404(Attachment, pk=pk)
    types_to_open = ('application/pdf', 'application/msword', )
    if attachment.mime_type in types_to_open:
        with open(attachment.attachment.path) as pdf:
            response = HttpResponse(pdf.read(), content_type=attachment.mime_type)
            response['Content-Disposition'] = 'inline;filename={}'.format(
                attachment.attachment.name.split('/')[-1])
            return response
        pdf.closed
    else:
        response = HttpResponse(attachment.attachment.open(),
                            content_type=attachment.mime_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % attachment
    return response


class AttachmentListView(SingleObjectMixin, View):
    """ List all attachments related to particular project.
    """
    model = SocialProject
    slug_url_kwarg = 'project_slug'
    template_name = 'projects/attachment_list.html'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(AttachmentListView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['object_list'] = self.object.attachments.all()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(AttachmentListView, self).get_context_data(**kwargs)
        context.update({
            'location': self.object.location,
            'is_moderator': is_moderator(self.request.user,
                                         self.object.location),
            'project_access': check_access(self.object, self.request.user), })
        return context


class AttachmentUpladView(LoginRequiredMixin, SingleObjectMixin, View):
    """ Grant access for attachment uploader.
    """
    model = SocialProject
    template_name = 'projects/attachment_form.html'
    form_class = AttachmentUploadForm

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not check_access(self.object, self.request.user):
            raise PermissionDenied
        return super(AttachmentUpladView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AttachmentUpladView, self).get_context_data(**kwargs)
        context.update({
            'location': self.object.location,
            'project_access': check_access(self.object, self.request.user), })
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class(initial={'project': self.object, })
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)
        obj = form.save(commit=False)
        obj.uploaded_by = self.request.user
        obj.save()
        messages.add_message(request, messages.SUCCESS, _(u"Files uploaded"))
        return redirect(obj.project.get_absolute_url())
