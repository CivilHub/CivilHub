# -*- coding: utf-8 -*-
import json

from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType

from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import ugettext as _

from actstream import action

from comments.models import CustomComment
from locations.mixins import LocationContextMixin, SearchableListMixin
from locations.links import LINKS_MAP as links
from maps.forms import AjaxPointerForm
from maps.models import MapPointer
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator

from .models import Idea, Vote, Category
from .forms import IdeaForm, CategoryForm


class IdeasContextMixin(LocationContextMixin):
    """
    Provides additional variables in the context connected with the localization of object(s).
    """
    def get_context_data(self):
        context = super(IdeasContextMixin, self).get_context_data()
        context['links'] = links['ideas']
        return context


def vote(request):
    """ Make vote (up/down) on idea. """
    if request.method == 'POST':
        idea = Idea.objects.get(pk=request.POST['idea'])
        votes_check = Vote.objects.filter(user=request.user).filter(idea=idea)
        if len(votes_check) > 0:
            response = {
                'success': False,
                'message': _('You voted already on this idea'),
                'votes': idea.get_votes(),
            }
        else:
            user_vote = Vote(
                user = request.user,
                idea = idea,
                vote = True if request.POST.get('vote') == 'up' else False
            )
            user_vote.save()
            response = {
                'success': True,
                'message': _('Vote saved'),
                'votes': idea.get_votes(),
            }
            action.send(
                request.user,
                action_object=user_vote,
                target=user_vote.idea,
                verb= _('voted on'),
                vote = True if request.POST.get('vote') == 'up' else False
            )
            request.user.profile.rank_pts += 1
            request.user.profile.save()
        return HttpResponse(json.dumps(response), content_type="application/json")


class CreateCategory(LoginRequiredMixin, CreateView):
    """
    Create new category for ideas.
    """
    model = Category
    template_name = 'ideas/category-create.html'
    form_class = CategoryForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        context = super(CreateCategory, self).get_context_data(**kwargs)
        context['title'] = _('Create new category')
        return context


class IdeasListView(IdeasContextMixin, SearchableListMixin):
    """ List all ideas """
    model = Idea
    paginate_by = 25

    def get_context_data(self):
        context = super(IdeasListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        qs = super(IdeasListView, self).get_queryset()
        status = self.request.GET.get('status', 'all')
        if status == 'True':
            qs = qs.filter(status=True)
        elif status == 'False':
            qs = qs.filter(status=False)
        return qs.filter(name__icontains=self.request.GET.get('haystack', ''))


class IdeasDetailView(DetailView):
    """ Detailed idea view. """
    model = Idea

    def get_object(self):
        object = super(IdeasDetailView, self).get_object()
        try:
            object.votes = get_votes(object)
            content_type = ContentType.objects.get_for_model(Idea)
            object.content_type = content_type.pk
            comment_set = CustomComment.objects.filter(
                content_type=content_type.pk
            )
            comment_set = comment_set.filter(object_pk=object.pk)
            object.comments = len(comment_set)
        except:
            object.votes = _('no votes yet')
        return object

    def get_context_data(self, **kwargs):
        context = super(IdeasDetailView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        context['title'] = self.object.name + " | " + self.object.location.name + " - Civilhub.org"
        context['location'] = self.object.location
        context['links'] = links['ideas']
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(self.object),
                'object_pk'   : self.object.pk,
            })
        return context


class CreateIdeaView(CreateView):
    """ Allow users to create new ideas. """
    model = Idea
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(CreateIdeaView, self).get_context_data(**kwargs)
        context['title'] = _('create new idea')
        context['action'] = 'create'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.edited = False
        obj.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        return super(CreateIdeaView, self).form_valid(form)


class UpdateIdeaView(UpdateView):
    """ Update existing idea details. """
    model = Idea
    form_class = IdeaForm
    template_name = 'locations/location_idea_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateIdeaView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        if self.object.creator != self.request.user and not context['is_moderator']:
            raise PermissionDenied
        context['location'] = self.object.location
        context['title'] = self.object.name
        context['action'] = 'update'
        context['links'] = links['ideas']
        return context

    def form_valid(self, form):
        form.instance.edited = True
        form.date_edited = timezone.now()
        return super(UpdateIdeaView, self).form_valid(form)
