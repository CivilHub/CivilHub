# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from etherpad.forms import ServePadForm
from etherpad.models import Pad
from locations.mixins import LocationContextMixin

from ..forms import DocumentForm
from ..models import SocialProject


class ProjectDocumentsList(ListView):
    """ List all documents created for this project. """
    model = Pad
    paginate_by = 25

    def get_queryset(self):
        project = get_object_or_404(SocialProject,
                                    slug=self.kwargs.get('slug'))
        return self.model.objects.filter(group=project.authors_group)

    def get_context_data(self):
        context = super(ProjectDocumentsList, self).get_context_data()
        project = get_object_or_404(SocialProject,
                                    slug=self.kwargs.get('slug'))
        context['object'] = project
        context['location'] = project.location
        context['document_form'] = DocumentForm(
            initial={'group': project.authors_group})
        return context


class ProjectDocumentPreview(LocationContextMixin, DetailView):
    """ Show single document in HTML format. """
    model = SocialProject
    template_name = 'projects/document_preview.html'

    def get_context_data(self, object=None):
        context = super(ProjectDocumentPreview, self).get_context_data()
        document_slug = self.kwargs.get('document_slug')
        context['document'] = get_object_or_404(Pad, slug=document_slug)
        context['location'] = self.object.location
        context['download_form'] = ServePadForm(
            initial={'pad': context['document'], })
        return context
