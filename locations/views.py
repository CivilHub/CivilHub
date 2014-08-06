# -*- coding: utf-8 -*-
import json, datetime, os
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
from forms import *
from models import Location
from .links import LINKS_MAP as links
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin
# Activity stream
from actstream.actions import follow, unfollow
from actstream.models import Action
# custom permissions
from places_core.permissions import is_moderator
from places_core.helpers import TagFilter, process_background_image
# REST views
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from geobase.models import Country
from locations.serializers import MapLocationSerializer
from .serializers import SimpleLocationSerializer


class LocationAPIViewSet(viewsets.ModelViewSet):
    """
    REST view for mobile app. Provides a way to manage and add new locations.
    """
    model = Location
    serializer_class = SimpleLocationSerializer
    paginate_by = 25
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)


class LocationMapViewSet(viewsets.ModelViewSet):
    """
    Prosty serializer dla mapy. Przechowuje tylko podstawowe informacje o lo-
    kalizacji, czyli id, długość oraz szerokość geograficzną i typ zawartości
    (żeby sobie później ułatwić doczytywanie/segregowanie obiektów na mapie).
    Tylko zapytania typu GET! Serializer niejako sztucznie dopasowuje infor-
    macje o obiekcie na wzór obiektów z mapy (markerów), dając do dyspozycji
    ten sam szkielet modelu do Backbone.
    
    Umożliwia wyszukiwanie na podstawie kodu kraju (country_code), np:
    `?code=pl`
    zwróci wszystkie lokalizacje w Polsce.
    """
    queryset = Location.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    serializer_class = MapLocationSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        code = self.request.QUERY_PARAMS.get('code')
        if code:
            locations = []
            parent_location = Country.objects.get(code=code.upper()).location
            if parent_location.latitude and parent_location.longitude:
                locations.append(parent_location)
            queryset = Location.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
            for l in queryset:
                if l in parent_location.get_ancestor_chain(response='QUERYSET'):
                    locations.append(l)
            return locations
        else:
            return Location.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)

class LocationNewsList(DetailView):
    """
    Location news page
    """
    model = Location
    template_name = 'locations/location_news.html'

    def get_context_data(self, **kwargs):
        context = super(LocationNewsList, self).get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['title'] = self.object.name + ', ' + _("News")
        context['links'] = links['news']
        context['tags'] = TagFilter(self.object).get_items()
        return context


class LocationNewsCreate(LoginRequiredMixin, CreateView):
    """
    Auto-fill some options in this view to create news in currently selected
    location etc.
    """
    model = News
    form_class    = NewsLocationForm
    template_name = 'locations/location_news_form.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        ctx = {
                'title': _('Create new entry'),
                'location': Location.objects.get(slug=slug),
                'links': links['news'],
                'appname': 'news-create',
                'form': NewsLocationForm(initial={
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
        return redirect(reverse('locations:news',
                        kwargs={'slug': obj.location.slug}))

    def form_invalid(self, form):
        ctx = {
                'title': _('Create new entry'),
                'location': form.cleaned_data.get('location'),
                'form': self.form_class(self.request.POST),
                'errors': form.errors,
                'appname': 'news-create',
                'user': self.request.user,
            }
        return render(self.request, self.template_name, ctx)


class LocationIdeasList(DetailView):
    """
    Location ideas list
    """
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
        if self.request.GET.get('order'):
            ideas = self.list_ideas(ideas, self.request.GET.get('order'))
        if self.request.GET.get('filter'):
            ideas = self.filter_ideas(ideas, self.request.GET.get('filter'))
        context['title'] = self.object.name + ', ' + _("Ideas") + " | CivilHub"
        context['form'] = IdeaCategoryForm()
        context['ideas'] = ideas
        context['links'] = links['ideas']
        context['appname'] = 'idea-list'
        context['categories'] = IdeaCategory.objects.all()
        context['tags'] = TagFilter(self.object).get_items()
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
        discussions = Discussion.objects.filter(location=location)
        paginator   = Paginator(discussions, 50)
        page = self.request.GET.get('page')

        try:
            context['discussions'] = paginator.page(page)
        except PageNotAnInteger:
            context['discussions'] = paginator.page(1)
        except EmptyPage:
            context['discussions'] = paginator.page(paginator.num_pages)

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
    location = Location.objects.get(slug=slug)
    queryset = Discussion.objects.filter(location=location)
    categories = ForumCategory.objects.all()
    category = request.GET.get('category')
    meta     = request.GET.get('meta')
    state    = request.GET.get('state')
    time     = request.GET.get('time')
    page     = request.GET.get('page')
    text     = request.GET.get('text')
    
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

    paginator = Paginator(queryset, 50)

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
        topic = Discussion.objects.latest('pk')
        lat = self.request.POST.get('latitude')
        lon = self.request.POST.get('longitude')
        if lat and lon:
            mp = MapPointer.objects.create(
                content_object = topic,
                latitude = lat,
                longitude = lon
            )
            mp.save()
            mp = MapPointer.objects.latest('pk')
            from geobase.storage import CountryJSONStorage
            cjs = CountryJSONStorage()
            cjs.dump_data(topic.location.country_code, False, True)
        super(LocationDiscussionCreate, self).form_valid(form)
        return redirect(reverse('locations:topic', 
            kwargs = {
                'place_slug': topic.location.slug,
                'slug': topic.slug,
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
        sublocations = self.object.get_ancestor_chain()
        max_per_page = 25
        paginator    = Paginator(sublocations, max_per_page)
        context      = {}
        page         = self.request.GET.get('page')

        try:
            context['sublocations'] = paginator.page(page)
        except PageNotAnInteger:
            context['sublocations'] = paginator.page(1)
        except EmptyPage:
            context['sublocations'] = paginator.page(paginator.num_pages)

        if len(context['sublocations']) <= max_per_page:
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
            obj.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
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
        context['title'] = 'Locations'
        return context


class LocationDetailView(DetailView):
    """
    Detailed location view
    """
    model = Location
    
    def get_context_data(self, **kwargs):
        location = super(LocationDetailView, self).get_object()
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(location)
        actions = Action.objects.filter(target_content_type=content_type)
        actions = actions.filter(target_object_id=location.pk)
        context['title'] = location.name
        context['actions'] = actions
        context['links'] = links['summary']
        context['appname'] = 'location'
        context['tags'] = TagFilter(self.object).get_items()
        return context


class CreateLocationView(LoginRequiredMixin, CreateView):
    """
    Add new location
    """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude', 'image']
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = super(CreateLocationView, self).get_context_data(**kwargs)
        context['title'] = _('create new location')
        return context

    def form_valid(self, form):
        if form.instance.latitude and form.instance.longitude:
            from geobase.storage import CountryJSONStorage
            cjs = CountryJSONStorage()
            cjs.dump_data(form.instance.country_code, True, False)
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
            tag = Tag.objects.get(name=tag)
            all_items = tag.taggit_taggeditem_items.all()
            for itm in all_items:
                if itm.content_object.location == location:
                    items.append(itm.content_object)

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
        location = Location.objects.get(slug=slug)
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
                context['tags']: TagFilter(location).get_items()
            })


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
    if not user.is_superuser and not location in user.mod_areas.all():
        return HttpResponseForbidden()
    img = process_background_image(request.FILES['background'], 'img/locations')
    try:
        os.unlink(location.image.path)
    except Exception:
        pass
    location.image = img
    location.save()
    return redirect(request.META['HTTP_REFERER'])
