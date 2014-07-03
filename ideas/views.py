# -*- coding: utf-8 -*-
import json, datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
# Use generic django views
from django.views.generic import View, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
from actstream import action
# Application native models
from userspace.models import UserProfile
from models import Idea, Vote, Category
from forms import IdeaForm, CategoryForm
from maps.forms import AjaxPointerForm
from maps.models import MapPointer
from locations.models import Location
from places_core.mixins import LoginRequiredMixin
from places_core.helpers import SimplePaginator, truncatehtml
# Custom comments
from comments.models import CustomComment
# Custom permissions
from places_core.permissions import is_moderator


def get_votes(idea):
    """
    Get total votes calculated for particular Idea object.
    """
    votes_total = Vote.objects.filter(idea=idea)
    votes_up    = len(votes_total.filter(vote=True))
    votes_down  = len(votes_total.filter(vote=False))
    return votes_up - votes_down


def vote(request):
    """
    Make vote (up/down) on idea
    """
    if request.method == 'POST':
        idea = Idea.objects.get(pk=request.POST['idea'])
        votes_check = Vote.objects.filter(user=request.user).filter(idea=idea)
        if len(votes_check) > 0:
            response = {
                'success': False,
                'message': 'You voted already on this idea',
                'votes': get_votes(idea),
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
                'message': 'Vote saved',
                'votes': get_votes(idea),
            }
            action.send(request.user, action_object=idea, verb='voted on')
            request.user.profile.rank_pts += 1
            request.user.profile.save()
        return HttpResponse(json.dumps(response))


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
            return HttpResponseNotAllowed
        context = super(CreateCategory, self).get_context_data(**kwargs)
        context['title'] = _('Create new category')
        return context


class BasicIdeaSerializer(object):
    """
    This is custom serializer for ideas. It passes properly formatted objects
    that they can be later dumped to JSON format. It gets Idea object instance
    as mandatory argument.
    
    For now this method supports only serializing - deserializing should be
    added later if needed.
    """
    def __init__(self, idea):
        tags = []

        for tag in idea.tags.all():
            tags.append({
                'name': tag.name,
                'url': reverse('locations:tag_search',
                               kwargs={'slug':idea.location.slug,
                                       'tag':tag.name})
            })

        self.data = {
            'id'            : idea.pk,
            'name'          : idea.name,
            'status'        : idea.status,
            'link'          : idea.get_absolute_url(),
            'description'   : truncatehtml(idea.description, 240),
            'creator'       : idea.creator.get_full_name(),
            'creator_url'   : idea.creator.profile.get_absolute_url(),
            'creator_id'    : idea.creator.pk,
            'avatar'        : idea.creator.profile.avatar.url,
            'date_created'  : timesince(idea.date_created),
            'edited'        : idea.edited,
            'total_votes'   : idea.get_votes(),
            'total_comments': idea.get_comment_count(),
            'tags'          : tags,
        }

        self.data['edit_url'] = reverse('ideas:update', kwargs={
            'slug': idea.slug,
        })

        try:
            self.data['date_edited'] = timesince(idea.date_edited)
        except Exception:
            self.data['date_edited'] = ''

        if idea.category:
            self.data['category']     = idea.category.name
            self.data['category_url'] = reverse('locations:category_search',
                kwargs={
                    'slug'    : idea.location.slug,
                    'app'     : 'ideas',
                    'model'   : 'idea',
                    'category': idea.category.pk,
                })
        else:
            self.data['category'] = ''
            self.data['category_url'] = ''

    def as_array(self):
        return self.data


class BasicIdeaView(View):
    """
    This is view for idea collection of one location. It is intended to return
    list of ideas formatted as JSON.
    """
    @classmethod
    def get_queryset(cls, request, queryset):
        """
        Filter queryset according to search options provided by user. This me-
        thod takes request and queryset to sort as parameters. All filters 
        should be set in GET parameters.
        """
        status = request.GET.get('status')
        if status == 'False':
            queryset = queryset.filter(status=False)
        elif status == 'True':
            queryset = queryset.filter(status=True)

        if request.GET.get('category') and request.GET.get('category') != 'all':
            category = Category.objects.get(pk=request.GET.get('category'))
            queryset = queryset.filter(category=category)

        time_delta = None
        time = request.GET.get('time')

        if time == 'day':
            time_delta = datetime.date.today() - datetime.timedelta(days=1)
        if time == 'week':
            time_delta = datetime.date.today() - datetime.timedelta(days=7)
        if time == 'month':
            time_delta = datetime.date.today() - relativedelta(months=1)
        if time == 'year':
            time_delta = datetime.date.today() - relativedelta(years=1)

        if time_delta:
            queryset = queryset.filter(date_created__gte=time_delta)

        haystack = request.GET.get('haystack')
        if haystack and haystack != 'false':
            queryset = queryset.filter(name__icontains=haystack)

        order = request.GET.get('order')
        if order == 'title':
            return queryset.order_by('name')
        elif order == 'date':
            return queryset.order_by('-date_created')
        elif order == 'category':
            return queryset.order_by('category__name')
        elif order == 'username':
            l = list(queryset);
            # Order by last name - we assume that every user has full name
            l.sort(key=lambda x: x.creator.get_full_name().split(' ')[1])
            return l
        elif order == 'votes':
            l = list(queryset);
            l.sort(key=lambda x: x.get_votes())
            return l
        else:
            return queryset

    def get(self, request, slug=None, *args, **kwargs):
        """
        Get list of all ideas or just idea set for one location if 'slug' is
        provided (default None).
        """
        if not slug:
            ideas = Idea.objects.all()
        else:
            location = Location.objects.get(slug=slug)
            ideas = Idea.objects.filter(location=location)

        ideas = self.get_queryset(request, ideas)
        ctx = {'results': []}

        for idea in ideas:
            ctx['results'].append(BasicIdeaSerializer(idea).data)

        paginator = SimplePaginator(ctx['results'], 15)
        page = request.GET.get('page') if request.GET.get('page') else 1
        ctx['current_page'] = page
        ctx['total_pages'] = paginator.count()
        ctx['results'] = paginator.page(page)

        return HttpResponse(json.dumps(ctx))


class IdeasListView(ListView):
    """
    List all ideas
    """
    model = Idea
    context_object_name = 'ideas'


class IdeasDetailView(DetailView):
    """
    Detailed idea view
    """
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
        context['title'] = self.object.name
        context['location'] = self.object.location
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(self.object)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(self.object),
                'object_pk'   : self.object.pk,
            })
        return context


class CreateIdeaView(CreateView):
    """
    Allow users to create new ideas
    """
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
    """
    Update existing idea details
    """
    model = Idea
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(UpdateIdeaView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        if self.object.creator != self.request.user and not context['is_moderator']:
            raise PermissionDenied
        context['location'] = self.object.location
        context['title'] = self.object.name
        context['action'] = 'update'
        return context

    def form_valid(self, form):
        form.instance.edited = True
        form.date_edited = timezone.now()
        return super(UpdateIdeaView, self).form_valid(form)


class DeleteIdeaView(DeleteView):
    """
    Allow users to delete their ideas (or not? Still not working).
    """
    model = Idea
    success_url = reverse_lazy('ideas:index')
