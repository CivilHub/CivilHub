# -*- coding: utf-8 -*-
import json, datetime, os
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, \
                        Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import cache
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag
from actstream import action
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from ideas.forms import CategoryForm as IdeaCategoryForm
from blog.models import News
from blog.models import Category as BlogCategory
from topics.models import Discussion, Entry
from topics.models import Category as ForumCategory
from polls.models import Poll, Answer
from polls.forms import PollForm
from civmail import messages as mails
from maps.models import MapPointer
from gallery.forms import BackgroundForm
from forms import *
from models import Location, Country
from .links import LINKS_MAP as links
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin
# Activity stream
from actstream.actions import follow, unfollow
from actstream.models import Action
# custom permissions
from places_core.permissions import is_moderator
from places_core.helpers import TagFilter, process_background_image, \
                sort_by_locale, get_time_difference
# REST views
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions as rest_permissions
from rest_framework.response import Response
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from locations.serializers import MapLocationSerializer
from .serializers import SimpleLocationSerializer, LocationListSerializer, \
                          CountrySerializer, ContentPaginatedSerializer
from rest.serializers import MyActionsSerializer, PaginatedActionSerializer

redis_cache = cache.get_cache('default')


class LocationIdeasList(DetailView):
    """ Location ideas list. """
    model = Location
    template_name = 'locations/location_ideas.html'

    @classmethod
    def list_ideas(cls, queryset, order):
        """ Order ideas list by few different keys. """
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

    @classmethod
    def filter_ideas(cls, queryset, filter):
        """ Filter ideas queryset to exclude unnecessary entries. """
        if filter == 'true':
            return queryset.filter(status=True)
        elif filter == 'false':
            return queryset.filter(status=False)
        else:
            return queryset.filter(name__icontains=filter)

    def get_context_data(self, **kwargs):
        context = super(LocationIdeasList, self).get_context_data(**kwargs)
        ideas = self.object.idea_set.all()
        context['title'] = self.object.name + ', ' + _("Ideas") + " | CivilHub"
        context['form'] = IdeaCategoryForm()
        context['ideas'] = True
        context['links'] = links['ideas']
        context['appname'] = 'idea-list'
        context['categories'] = IdeaCategory.objects.all()
        #context['tags'] = TagFilter(self.object).get_items()
        return context


class LocationIdeaCreate(LoginRequiredMixin, CreateView):
    """
    Create new idea in scope of currently selected location.
    """
    model = Idea
    form_class = IdeaLocationForm
    template_name = 'locations/location_idea_form.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        ctx = {
                'location': Location.objects.get(slug=slug),
                'title': _("Create new idea"),
                'links': links['ideas'],
                'appname': 'idea-create',
                'form': IdeaLocationForm(initial={
                    'location': Location.objects.get(slug=slug)
                })
            }
        return render(request, self.template_name, ctx)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        try:
            for m in json.loads(self.request.POST.get('markers')):
                marker = MapPointer.objects.create(
                    content_type=ContentType.objects.get_for_model(Idea),
                    object_pk=obj.pk, latitude=m['lat'], longitude=m['lng'])
        except Exception:
            # FIXME: silent fail, powinna być flash message
            pass
        return super(LocationIdeaCreate, self).form_valid(form)

    def form_invalid(self, form):
        ctx = {
                'title': _('Create new idea'),
                'location': form.cleaned_data.get('location'),
                'form': self.form_class(self.request.POST),
                'errors': form.errors,
                'user': self.request.user,
                'appname': 'idea-create',
                'links': links['ideas'],
            }
        return render(self.request, self.template_name, ctx)


class LocationDiscussionsList(DetailView):
    """
    Get list of all discussion topics related to this location.
    """
    model = Location
    template_name = 'locations/location_forum.html'

    def get_context_data(self, **kwargs):
        location = super(LocationDiscussionsList, self).get_object()
        context  = super(LocationDiscussionsList, self).get_context_data(**kwargs)
        context['discussions'] = True
        context['title']        = location.name + ", " + _("Discussions") + " | CivilHub"
        context['categories']   = ForumCategory.objects.all()
        context['search_form']  = SearchDiscussionForm()
        context['is_moderator'] = is_moderator(self.request.user, location)
        context['links']        = links['discussions']
        context['tags'] = TagFilter(location).get_items()
        return context


def ajax_discussion_list(request, slug):
    """
    "Ulepszenie" filtrowania wyników dla klientów korzystających
    z Javascript.
    """
    try:
        location = Location.objects.get(slug=slug)
        queryset = Discussion.objects.filter(location=location)
        categories = ForumCategory.objects.all()
        category = request.GET.get('category')
        meta     = request.GET.get('meta')
        state    = request.GET.get('state')
        time     = request.GET.get('time')
        page     = request.GET.get('page')
        text     = request.GET.get('text')
    except Location.DoesNotExist:
        location = None
    
    if location is None or not request.is_ajax():
        raise Http404()
    
    if category != 'all':
        queryset = queryset.filter(category=category)

    if state != 'all':
        queryset = queryset.filter(status=state)

    if text and text != 'false':
        queryset = queryset.filter(question__contains=text)

    time_delta = None

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

    if meta:
        queryset = queryset.order_by(meta)

    paginator = Paginator(queryset, settings.LIST_PAGINATION_LIMIT)

    context = {}

    try:
        context['discussions'] = paginator.page(page)
    except PageNotAnInteger:
        context['discussions'] = paginator.page(1)
    except EmptyPage:
        context['discussions'] = paginator.page(paginator.num_pages)

    context['title']        = location.name + ', ' + _('Discussions')
    context['location']     = location
    context['categories']   = categories
    context['search_form']  = SearchDiscussionForm()
    context['is_moderator'] = is_moderator(request.user, location)
    context['links']        = links['discussions']
    context['appname']      = 'discussion-list'
    context['tags'] = TagFilter(location).get_items()

    return render(request, 'locations/location_forum.html', context)


class LocationDiscussionCreate(LoginRequiredMixin, CreateView):
    """
    Custom form to auto-fill fields related with location.
    """
    model = Discussion
    form_class = DiscussionLocationForm
    template_name = 'locations/location_forum_create.html'
    parent_object = None

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        self.parent_object = Location.objects.get(slug=slug) 
        ctx = {
                'title': _('Create new discussion'),
                'location': self.parent_object,
                'links': links['discussions'],
                'appname': 'discussion-create',
                'form': DiscussionLocationForm(initial={
                    'location': Location.objects.get(slug=slug)
                })
            }
        return render(request, self.template_name, ctx)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        try:
            for m in json.loads(self.request.POST.get('markers')):
                marker = MapPointer.objects.create(
                    content_type=ContentType.objects.get_for_model(Discussion),
                    object_pk=obj.pk, latitude=m['lat'], longitude=m['lng'])
        except Exception:
            # FIXME: silent fail, powinna być flash message
            pass
        return redirect(reverse('locations:topic', 
            kwargs = {
                'place_slug': obj.location.slug,
                'slug': obj.slug,
            }
        ))

    def form_invalid(self, form):
        context = {}
        context['location'] = form.instance.location
        context['user'] = self.request.user
        context['form'] = DiscussionLocationForm(self.request.POST)
        context['links'] = links['discussions']
        context['title'] = _("Create new discussion")
        context['appname'] = 'discussion-create'
        return render(self.request, self.template_name, context)


class SublocationList(DetailView):
    """
    Strona zawiera listę lokalizacji, dla których bieżąca lokalizacja
    jest lokalizacją macierzystą.
    """
    model = Location
    template_name = 'locations/sublocation-list.html'

    def get_context_data(self, **kwargs):
        context = super(SublocationList, self).get_context_data(**kwargs)
        sublocations = self.object.location_set.all()
        max_per_page = 24
        paginator    = Paginator(sublocations, max_per_page)
        context      = {}
        page         = self.request.GET.get('page')

        try:
            context['sublocations'] = paginator.page(page)
        except PageNotAnInteger:
            context['sublocations'] = paginator.page(1)
        except EmptyPage:
            context['sublocations'] = paginator.page(paginator.num_pages)

        if paginator.num_pages <= max_per_page:
            context['navigation'] = False
        else:
            context['navigation'] = True

        context['title']    = self.object.name + ', ' + _("Sublocations")
        context['location'] = self.object
        context['links']    = links['sublocations']
        context['tags'] = TagFilter(self.object).get_items()
        return context


class LocationFollowersList(DetailView):
    """
    Location followers list
    """
    model = Location
    template_name = 'locations/location_followers.html'

    def get_context_data(self, **kwargs):
        context = super(LocationFollowersList, self).get_context_data(**kwargs)
        
        followers = self.object.users.all()
        max_per_page = settings.LIST_PAGINATION_LIMIT
        paginator    = Paginator(followers, max_per_page)
        page         = self.request.GET.get('page')

        try:
            context['followers'] = paginator.page(page)
        except PageNotAnInteger:
            context['followers'] = paginator.page(1)
        except EmptyPage:
            context['followers'] = paginator.page(paginator.num_pages)

        if paginator.num_pages <= max_per_page:
            context['navigation'] = False
        else:
            context['navigation'] = True
            
        context['title'] = self.object.name + ', ' + _("Followers")
        context['is_moderator'] = is_moderator(self.request.user, self.object)
        context['top_followers'] = self.object.most_active_followers()
        context['links'] = links['followers']
        context['tags'] = TagFilter(self.object).get_items()
        return context


class LocationPollsList(DetailView):
    """
    Show list of polls made in this location.
    """
    model = Location
    template_name = 'locations/location_polls.html'

    def get_context_data(self, **kwargs):
        location = super(LocationPollsList, self).get_object()
        context = super(LocationPollsList, self).get_context_data(**kwargs)
        context['title'] = location.name + ', ' + _('Polls')
        context['polls'] = Poll.objects.filter(location=location)
        context['links'] = links['polls']
        context['is_moderator'] = is_moderator(self.request.user, location)
        context['tags'] = TagFilter(self.object).get_items()
        return context


class LocationPollCreate(LoginRequiredMixin, CreateView):
    """
    Create poll in currently selected location.
    """
    model = Poll
    form_class = PollForm
    template_name = 'polls/create-poll.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        location = Location.objects.get(slug=slug)
        ctx = {
                'title': _('Create new poll'),
                'location': location,
                'links': links['polls'],
                'appname': 'poll-create',
                'form': PollForm(initial={
                    'location': location
                })
            }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = self.request.user
            obj.image = request.FILES.get('image')
            obj.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            for f in request.FILES: print f
            for key, val in request.POST.iteritems():
                if 'answer_txt_' in key:
                    a = Answer(poll=obj, answer=val)
                    a.save()
            return redirect(obj.get_absolute_url())
        else:
            context = {
                'title': _('Create new poll'),
                'location': form.cleaned_data['location'],
                'links': links['polls'],
                'appname': 'poll-create',
                'form': PollForm(request.POST),
            }
            return render(request, self.template_name, context)

    def form_invalid(self, form):
        context = super(LocationPollCreate, self).get_context_data(form=form)
        context['location'] = Location.objects.get(pk=self.request.POST.get('location'))
        context['user']  = self.request.user
        context['form']  = self.form_class(self.request.POST)
        context['links'] = links['polls']
        context['title'] = _("Create new poll")
        context['appname'] = 'poll-create'
        return render(self.request, self.template_name, context)


class LocationListView(ListView):
    """
    Location list
    """
    model = Location
    context_object_name = 'locations'
    template_name = 'location_list.html'
    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['title'] = _(u'Locations')
        return context


def get_latest(location, item_type):
    """ Get latest item from location set. """
    if item_type == 'blog':
        lset = location.news_set.all().distinct()
    elif item_type == 'ideas':
        lset = location.idea_set.all().distinct()
    elif item_type == 'topics':
        lset = location.discussion_set.all().distinct()
    elif item_type == 'polls':
        lset = location.poll_set.all().distinct()
    return lset.order_by('-date_created')[:5]


class LocationDetailView(DetailView):
    """ Detailed location view. """
    model = Location
    
    def get_context_data(self, **kwargs):
        #location = super(LocationDetailView, self).get_object()
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        #content_type = ContentType.objects.get_for_model(location)
        #actions = Action.objects.filter(target_content_type=content_type)
        #actions = actions.filter(target_object_id=location.pk)
        context['title'] = self.object.name
        #context['actions'] = actions
        #context['tags'] = TagFilter(self.object).get_items()
        # context['blog'] = get_latest(location, 'blog')
        # context['ideas'] = get_latest(location, 'ideas')
        # context['topics'] = get_latest(location, 'topics')
        # context['polls'] = get_latest(location, 'polls')
        context['is_moderator'] = is_moderator(self.request.user, self.object)
        return context


class LocationBackgroundView(FormView):
    """
    Formularz statyczny umożliwiający upload i przycinanie zdjęć tła dla
    lokalizacji.
    """
    template_name = 'locations/background-form.html'
    form_class = BackgroundForm

    def get_context_data(self, **kwargs):
        context = super(LocationBackgroundView, self).get_context_data(**kwargs)
        try:
            context['location'] = Location.objects.get(
                pk=self.kwargs.get('pk', None))
        except Location.DoesNotExist:
            raise Http404()
        return context

    def get(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404()
        user = request.user
        if not user.is_superuser and not is_moderator(user, location):
            raise Http404()
        return super(LocationBackgroundView, self).get(request, pk)

    def form_valid(self, form):
        from PIL import Image
        from gallery.image import handle_tmp_image
        box = (
            form.cleaned_data['x'],
            form.cleaned_data['y'],
            form.cleaned_data['x2'],
            form.cleaned_data['y2'],
        )
        image = Image.open(form.cleaned_data['image'])
        image = image.crop(box)
        location = Location.objects.get(pk=self.kwargs.get('pk', None))
        location.image = handle_tmp_image(image)
        location.save()
        return redirect(reverse('locations:details',
                         kwargs={'slug': location.slug}))


class CreateLocationView(LoginRequiredMixin, CreateView):
    """
    Add new location
    """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude', 'image']
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = super(CreateLocationView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['title'] = _('create new location')
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateLocationView, self).form_valid(form)


class UpdateLocationView(LoginRequiredMixin, UpdateView):
    """
    Update existing location
    """
    model = Location
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        location = super(UpdateLocationView, self).get_object()
        context = super(UpdateLocationView, self).get_context_data(**kwargs)
        context['title'] = location.name
        context['subtitle'] = _('Edit this location')
        context['action'] = 'edit'
        context['appname'] = 'location-create'
        return context


class DeleteLocationView(LoginRequiredMixin, DeleteView):
    """
    Delete location
    """
    model = Location
    success_url = reverse_lazy('locations:index')


class LocationContentSearch(View):
    """
    Strona z wynikami sortowania treści dla jednego taga. Zbieramy treści tylko
    z lokalizacji, którą aktualnie przegląda użytkownik.
    """
    http_method_names = [u'get']
    template_name     = 'locations/tag-search.html'

    def get(self, request, slug, tag=None):
        location = get_object_or_404(Location, slug=slug)
        t_filter = TagFilter(location)
        tags = t_filter.get_items()
        items = []

        if tag:
            try:
                tag = Tag.objects.get(slug=tag)
                all_items = tag.taggit_taggeditem_items.all()
            except Tag.DoesNotExist:
                all_items = []
            items = [x.content_object for x in all_items if x.content_object.location==location]

        return render(request, self.template_name, {
                'title'   : _("Search by tag"),
                'location': location,
                'items'   : items,
                'tags'    : tags,
            })


class LocationContentFilter(View):
    """
    Strona filtrowania treści w/g kategorii. Tego typu filtrowanie jest przy-
    datne tylko dla poszczególnych rodzajów treści. Jak powyżej, zbieramy
    treści tylko z aktualnie przeglądanej lokalizacji.
    """
    http_method_names = [u'get']
    template_name = 'locations/category-search.html'

    def get(self, request, slug, app, model, category):
        try:
            location = Location.objects.get(slug=slug)
        except Location.DoesNotExist:
            raise Http404()
        category_type = ContentType.objects.get(app_label=app, model='category')
        category_type = category_type.model_class()
        category = category_type.objects.get(pk=category)
        ct = ContentType.objects.get(app_label=app, model=model)
        ct = ct.model_class()
        items = ct.objects.filter(location=location).filter(category=category)

        return render(request, self.template_name, {
                'title'   : _("Search by category"),
                'location': location,
                'items'   : items,
                'tags'    : TagFilter(location).get_items()
            })


class LocationContentDelete(View):
    """
    Uniwersalny widok pozwalający administratorom oraz moderatorom usuwać treści
    z "podlegajęcej" im lokalizacji.
    """
    http_method_names = [u'get', u'post',]
    template_name = 'locations/content-remove.html'

    def get(self, request, content_type=None, object_pk=None):
        ct = ContentType.objects.get(pk=content_type)
        self.object = ct.get_object_for_this_type(pk=object_pk)
        context = {
            'title': _("Confirm delete"),
            'content_type': content_type,
            'object_pk': object_pk,
            'location': self.object.location,
        }
        return render(request, self.template_name, context)

    def post(self, request, content_type, object_pk):
        ct = ContentType.objects.get(pk=request.POST.get('content_type', None))
        self.object = ct.get_object_for_this_type(pk=request.POST.get('object_pk', None))
        if not request.user.is_superuser and not is_moderator(request.user, self.object.location):
            return HttpResponseNotFound()
        self.object.delete()
        return redirect(reverse('locations:details',
                         kwargs={'slug': self.object.location.slug}))


class InviteUsersView(LoginRequiredMixin, View):
    """
    Widok z myślą o formularzu zapraszania innych użytkowników do 'śledzenia'
    lokalizacji. Definiuje metody, które zwracają formularz dla modala oraz
    przesyłają maila do wybranych użytkowników.
    """
    http_method_names = [u'get', u'post']
    template_name = 'locations/invite-users.html'
    object = None

    def get_object(self, pk):
        """ Get location object from db. """
        if not self.object:
            self.object = Location.objects.get(pk=pk)
        return self.object

    def get(self, request, pk):
        """ Create invite form. """
        location = self.get_object(pk)
        form = InviteUsersForm(initial={'location': location})
        return render(request, self.template_name, {
            'location': location,
            'form': form,
        })

    def post(self, request, pk):
        """ Send message to selected users. """
        users = request.POST.getlist('user[]')
        if users:
            for u in users:
                user = User.objects.get(pk=u)
                translation.activate(user.profile.lang)
                # Send email
                email = mails.InviteUsersMail()
                email.send(user.email, {
                    'inviting_user': request.user,
                    'location': self.get_object(pk),
                })
                # Record action for actstream
                action.send(
                    request.user,
                    action_object = self.get_object(pk),
                    target = user,
                    verb = _("invited you to follow")
                )
            ctx = {
                'success': True,
                'message': _("Successfully send invitation"),
                'level'  : 'success',
            }
        else:
            ctx = {
                'success': False,
                'message': _("User field cannot be empty"),
                'level'  : 'danger',
            }
        return HttpResponse(json.dumps(ctx))


@login_required
@require_POST
def add_follower(request, pk):
    """
    Add user to locations followers
    """
    location = get_object_or_404(Location, pk=pk)
    user = request.user
    location.users.add(user)

    try:
        location.save()
        follow(user, location, actor_only = False)
        response = {
            'success': True,
            'message': _('You follow this location'),
        }
    except:
        response = {
            'success': False,
            'message': _('Something, somewhere went terribly wrong'),
        }
    return HttpResponse(json.dumps(response))


@login_required
@require_POST
def remove_follower(request, pk):
    """
    Remove user from locations followers
    """
    location = get_object_or_404(Location, pk=pk)
    user = request.user
    location.users.remove(user)
    try:
        location.save()
        unfollow(user, location)
        response = {
            'success': True,
            'message': _('You stop following this location'),
        }
    except:
        response = {
            'success': False,
            'message': _('Something, somewhere went terribly wrong'),
        }
    return HttpResponse(json.dumps(response))


@login_required
@require_POST
def change_background(request, pk):
    """ Change place picture with single button. """
    location = Location.objects.get(pk=pk)
    user = request.user
    if not user.is_superuser and not is_moderator(user, location):
        return HttpResponseForbidden()
    location.image = request.FILES['image']
    location.save()
    return redirect(request.META['HTTP_REFERER'])
