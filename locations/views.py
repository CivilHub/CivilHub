# -*- coding: utf-8 -*-
import json
import datetime
import os

from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.template.base import TemplateDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, \
                        Http404
from django.core import cache, serializers
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from taggit.models import Tag
from actstream import action
from actstream.actions import follow, unfollow
from actstream.models import Action, followers
from easy_pdf.views import PDFTemplateView

from blog.models import News
from blog.models import Category as BlogCategory
from civmail import messages as mails
from gallery.forms import BackgroundForm
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from ideas.forms import CategoryForm as IdeaCategoryForm
from maps.models import MapPointer
from notifications.models import notify
from organizations.forms import NGOSearchForm
from organizations.models import Organization
from places_core.helpers import TagFilter, process_background_image, \
                sort_by_locale, get_time_difference
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from polls.models import Poll, Answer
from polls.forms import PollForm
from topics.models import Discussion, Entry
from topics.models import Category as ForumCategory

from .charts import actions_chart, follow_chart, pie_chart, summary_chart
from .forms import *
from .helpers import move_location_contents
from .mixins import LocationContextMixin
from .models import Location, Country
from .links import LINKS_MAP as links

redis_cache = cache.get_cache('default')


def update_parent_location_list(location):
    """ Update cached sublocations for added or removed location parent. """
    if location.parent is not None and settings.USE_CACHE:
        for language in [x[0] for x in settings.LANGUAGES]:
            key = "{}_{}_sub".format(location.parent.slug, language)
            redis_cache.set(key, location.parent.location_set.all())


class LocationAccessMixin(SingleObjectMixin):
    """ Check user permissions for particular location. Made for update views. """
    def get_object(self):
        location = super(LocationAccessMixin, self).get_object()
        if not is_moderator(self.request.user, location):
            raise PermissionDenied
        return location


class LocationViewMixin(DetailView):
    """ Provides common context data for all presentaion views. """
    model = Location

    def get_context_data(self, **kwargs):
        context = super(LocationViewMixin, self).get_context_data(**kwargs)
        context['title'] = self.object.name
        context['is_moderator'] = is_moderator(self.request.user, self.object)
        return context


class LocationStatisticsView(LocationViewMixin):
    """
    """
    template_name = 'locations/statistics.html'

    def get_context_data(self, **kwargs):
        context = super(LocationStatisticsView, self).get_context_data(**kwargs)
        context.update({
            'pie_data': pie_chart(self.object),
            'summary_data': summary_chart(self.object),
            'timeline_data': actions_chart(self.object),
            'follower_data': follow_chart(self.object), })
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
                'location': get_object_or_404(Location, slug=slug),
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
    The site contains a list of locations for which the current location
    is the parent location.
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
    """ Location followers list
    """
    model = Location
    template_name = 'locations/location_followers.html'

    def get_followers(self):
        order = self.request.GET.get('order')
        qs = User.objects.filter(pk__in=[x.pk for x in followers(self.object)])
        if order == 'abc':
            return qs.order_by('first_name', 'last_name')
        else:
            return qs.order_by('-profile__rank_pts')

    def get_search_form(self):
        fields = [
            {'value': 'abc', 'label': _("Alphabetically"), },
            {'value': 'default', 'label': _("By profile points"), }, ]
        field_html = '<select name="order" class="form-control">'
        order = self.request.GET.get('order', 'default')
        for field in fields:
            field_html += '<option value="%s"' % field['value']
            if field['value'] == order:
                field_html += ' selected="selected"'
            field_html += '>%s</option>' % field['label']
        field_html += '</select>'
        return field_html

    def get_context_data(self, **kwargs):
        context = super(LocationFollowersList, self).get_context_data(**kwargs)
        max_per_page = settings.LIST_PAGINATION_LIMIT
        paginator = Paginator(self.get_followers(), max_per_page)
        page = self.request.GET.get('page')

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
        context['filter_form'] = self.get_search_form()
        print context['filter_form']
        context['is_moderator'] = is_moderator(self.request.user, self.object)
        context['top_followers'] = self.object.most_active_followers()
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
    """ List view for all locations. """
    model = Location
    context_object_name = 'locations'
    template_name = 'location_list.html'

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['title'] = _(u'Locations')
        return context

    def get(self, request):
        """ Returns results for autocomplete widget. """
        if request.is_ajax():
            fields = ('id', 'name', 'slug', 'parent', 'country_code',)
            term = request.GET.get('term', '')
            locations = self.model.objects.filter(name__icontains=term)
            context = serializers.serialize("json", locations, fields=fields)
            return HttpResponse(context, content_type="application/json")
        return super(LocationListView, self).get(request)


class LocationDetailView(LocationViewMixin):
    """ Detailed location view. """
    template_name = 'locations/location_detail.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['tags'] = TagFilter(self.object).get_items()
        return context


class LocationActionsView(LocationViewMixin):
    """ Various 'variations on the subject' i.e. 'subviews' for locations. """
    template_name = 'locations/location_summary.html'


class LocationBackgroundView(LoginRequiredMixin, LocationViewMixin, View):
    """ Advanced options for location background image. As we may create as many
        image files as we want, just one may be tied to location. Here we may
        update existing picture, choose from other uploaded pictures or upload
        entirely new file. Only admins and moderators can access this view.
    """
    template_name = 'locations/background.html'
    current_image_form = CurrentBackgroundForm

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not is_moderator(self.request.user, self.object):
            raise PermissionDenied
        return super(LocationBackgroundView, self).dispatch(*args, **kwargs)

    def get(self, request, slug=None, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, slug=None, **kwargs):
        form = self.current_image_form(request.POST,
                    instance=self.object.background)
        obj = form.save()
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(LocationBackgroundView, self).get_context_data()
        context['form'] = self.current_image_form(instance=self.object.background)
        return context


class LocationBackgroundUploadView(FormView):
    template_name = 'locations/background-form.html'
    form_class = BackgroundUploadForm

    def dispatch(self, *args, **kwargs):
        self.object = get_object_or_404(Location, pk=kwargs.get('pk'))
        return super(LocationBackgroundUploadView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context.update({'form': self.form_class, })
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(LocationBackgroundUploadView, self).get_context_data()
        context.update({
            'location': self.object,
            'is_moderator': is_moderator(self.request.user, self.object), })
        return context

    def form_valid(self, form):
        import pdb; pdb.set_trace()
        self.object.background = form.save()
        self.object.save()
        return super(LocationBackgroundUploadView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

# class LocationBackgroundUploadView(FormView):
#     """
#     A static form that allows to upload and crop background images for locations.
#     """
#     template_name = 'locations/background-form.html'
#     form_class = BackgroundForm

#     def get_context_data(self, **kwargs):
#         context = super(LocationBackgroundUploadView, self).get_context_data(**kwargs)
#         try:
#             context['location'] = Location.objects.get(
#                 pk=self.kwargs.get('pk', None))
#         except Location.DoesNotExist:
#             raise Http404()
#         return context

#     def get(self, request, pk=None):
#         try:
#             location = Location.objects.get(pk=pk)
#         except Location.DoesNotExist:
#             raise Http404()
#         user = request.user
#         if not user.is_superuser and not is_moderator(user, location):
#             raise Http404()
#         return super(LocationBackgroundUploadView, self).get(request, pk)

#     def form_valid(self, form):
#         from PIL import Image
#         from gallery.image import handle_tmp_image
#         box = (
#             form.cleaned_data['x'],
#             form.cleaned_data['y'],
#             form.cleaned_data['x2'],
#             form.cleaned_data['y2'],
#         )
#         image = Image.open(form.cleaned_data['image'])
#         image = image.crop(box)
#         location = Location.objects.get(pk=self.kwargs.get('pk', None))
#         location.image = handle_tmp_image(image)
#         location.save()
#         return redirect(reverse('locations:details',
#                          kwargs={'slug': location.slug}))


class CreateLocationView(LoginRequiredMixin, CreateView):
    """ Add new location. """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude']
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = super(CreateLocationView, self).get_context_data(**kwargs)
        context['countries'] = Location.objects.filter(kind='country')
        context['title'] = _('create new location')
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        parent = form.cleaned_data.get('parent')
        if parent is not None:
            parent = form.cleaned_data['parent']
            parent_id_list = [parent.pk, ] + parent.get_parents
            context['parents'] = Location.objects.filter(pk__in=parent_id_list)
        return super(CreateLocationView, self).render_to_response(context)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        obj = form.save()
        obj.creator.profile.mod_areas.add(obj)
        obj.creator.profile.save()
        update_parent_location_list(obj)
        return super(CreateLocationView, self).form_valid(form)


class UpdateLocationView(LocationAccessMixin, UpdateView):
    """ Update existing location. """
    model = Location
    form_class = LocationForm

    def get_form_kwargs(self):
        form_kwargs = super(UpdateLocationView, self).get_form_kwargs()
        form_kwargs.update({'user': self.request.user, })
        return form_kwargs

    def get_context_data(self, **kwargs):
        location = super(UpdateLocationView, self).get_object()
        context = super(UpdateLocationView, self).get_context_data(**kwargs)
        context['title'] = location.name
        context['countries'] = Country.objects.all()
        context['subtitle'] = _('Edit this location')
        context['action'] = 'edit'
        context['appname'] = 'location-create'
        if self.object.parent is None:
            parents = []
        else:
            parent = self.object.parent
            parent_id_list = [parent.pk, ] + parent.get_parents
            parents = [Location.objects.get(pk=x) for x in parent_id_list]
        context['parents'] = parents
        return context

    def form_valid(self, form):
        lang = translation.get_language_from_request(self.request)
        # Update translation in editing user's language
        for an in form.instance.names.filter(language=lang):
            an.altername = form.instance.name
            an.save()
        return super(UpdateLocationView, self).form_valid(form)


class DeleteLocationView(LoginRequiredMixin, DeleteView):
    """ Delete location. """
    model = Location
    success_url = reverse_lazy('locations:index')

    def post(self, request, slug=None):
        if not request.user.is_superuser:
            raise Http404
        try:
            location_pk = int(request.POST.get('new_location'))
            new_location = get_object_or_404(Location, pk=location_pk)
            move_location_contents(self.get_object(), new_location)
        except (ValueError, TypeError):
            # There is no other location selected
            pass
        return super(DeleteLocationView, self).post(request, slug)

    def get(self, request, slug=None):
        if not request.user.is_superuser:
            raise Http404
        return super(DeleteLocationView, self).get(request, slug)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        update_parent_location_list(self.object)
        return redirect(self.get_success_url())


class LocationContentSearch(View):
    """
    A site with the results of sorting content for one tag. We gather content
    only from the location that the user is currently viewing.
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
                'current_tag': tag, })


class LocationContentFilter(View):
    """
    A content filter by category site.This type of filtering is
    useful only for certain types of content. Same sa above, we
    only gather content from the location that the user is currently
    viewing.
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
    A universal view that allows the admins and mods to delete the content from
    "subject" locations.
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
    A view with the from of invite a other users to 'follow' a location in mind.
    It defines the methods that return the form for the modal and send an email
    to the chosen users.
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


class InviteUsersByEmailView(LoginRequiredMixin, FormView):
    """
    Invite users to follow selected location using only their email addresses.
    """
    template_name = 'locations/invite_by_email.html'
    form_class = InviteUsersByEmail
    location = None

    def dispatch(self, *args, **kwargs):
        self.location = get_object_or_404(Location, slug=kwargs['location_slug'])
        return super(InviteUsersByEmailView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.location.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(InviteUsersByEmailView, self).get_context_data(**kwargs)
        context.update({
            'location': self.location,
            'is_moderator': is_moderator(self.request.user, self.location),
        })
        return context

    def form_valid(self, form):
        for email in form.cleaned_data['emails']:
            message = mails.InviteUsersMail()
            message.send(email, {
                'lang': translation.get_language_from_request(self.request),
                'inviting_user': self.request.user,
                'location': self.location,
            })
        messages.add_message(self.request, messages.SUCCESS,
            _(u"All messages sent successfully"))
        return super(InviteUsersByEmailView, self).form_valid(form)


class PDFInviteGenerateView(SingleObjectMixin, PDFTemplateView):
    """
    This view presents PDF document with location details.
    """
    model = Location
    template_name = 'easy_pdf/invitation.html'

    def get_context_data(self):
        context = super(PDFInviteGenerateView, self).get_context_data()
        context['title'] = context['location'].__unicode__()
        context['font'] = os.path.join(settings.BASE_DIR,
            'places_core/static/places_core/fonts/Lato-Regular.ttf')
        context['img'] = os.path.join(settings.BASE_DIR,
            'templates/easy_pdf/img/bg_pdf.jpg')
        return context

    def get(self, request, slug):
        self.object = get_object_or_404(Location, slug=slug)
        return super(PDFInviteGenerateView, self).get(request, slug)


class ModeratorListAccessMixin(LocationContextMixin, View):
    """
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        self.location = self.get_current_location()
        return super(ModeratorListAccessMixin, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('locations:manage-moderators', kwargs={
            'location_slug': self.location.slug, })


class ManageModeratorsView(ModeratorListAccessMixin):
    """ Superuser may grant or revoke moderator status for other users.
    """
    template_name = 'locations/moderator_list.html'
    form_class = InviteUsersByEmail

    def get_context_data(self):
        context = super(ManageModeratorsView, self).get_context_data()
        context['moderators'] = [x for x in User.objects.filter(is_active=True)\
                                if self.location in x.profile.mod_areas.all()]
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        for user in User.objects.filter(email__in=form.cleaned_data['emails']):
            if not self.location in user.profile.mod_areas.all():
                user.profile.mod_areas.add(self.location)
                user.profile.save()
                notify(self.request.user, user,
                    verb=_(u"Granted you moderator access to"),
                    action_target=self.location)
        messages.add_message(request, messages.SUCCESS, _(u"Success"))
        return redirect(self.get_success_url())


class RemoveModeratorView(ModeratorListAccessMixin):
    """ Delete moderators using list.
    """
    def post(self, request, **kwargs):
        user = get_object_or_404(User, pk=request.POST.get('user_id'))
        if self.location in user.profile.mod_areas.all():
            user.profile.mod_areas.remove(self.location)
        return redirect(self.get_success_url())


# NGO related views
# -----------------


class LocationNGOList(LocationContextMixin, DetailView):
    """ List all organizations that patronate this location.
    """
    model = Location
    slug_url_kwarg = 'location_slug'
    template_name = 'locations/organization_list.html'
    form_class = NGOSearchForm

    def get_form(self):
        self.form =  self.form_class(self.request.GET)
        return self.form

    def get_ngo_list(self):
        qs = Organization.objects.filter(locations__in=[self.object, ])
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data.get('name')
            kind = form.cleaned_data.get('kind')
        if name:
            qs = qs.filter(name__icontains=name)
        if kind is not None:
            qs = qs.filter(category=kind)
        return qs.order_by('name').distinct()

    def get_context_data(self, **kwargs):
        context = super(LocationNGOList, self).get_context_data()
        context['form'] = self.get_form()
        context['object_list'] = self.get_ngo_list()
        return context


# Widget Factory views
# --------------------


class WidgetFactoryMixin(View):
    """ Provides a common way to get widget settings from requested url.
    """
    def get_widget_settings(self):
        ct = ContentType.objects.get(pk=self.kwargs.get('ct'))
        pk = self.kwargs.get('pk')
        try:
            self.object = ct.get_object_for_this_type(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return {
            'ct': ct.pk,
            'pk': pk,
            'div_id': "civil-widget-{}{}".format(ct.pk, pk),
            'lang': self.request.GET.get('lang', settings.LANGUAGE_CODE),
            'site': get_current_site(self.request),
            'width': str(self.request.GET.get('width', 400)),
        }

    def create_url(self):
        widget_settings = self.get_widget_settings()
        url_ctx = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': widget_settings['site'].domain,
            'path': reverse('locations:widget', kwargs={
                'ct': widget_settings['ct'], 'pk': widget_settings['pk'], }),
            'lang': widget_settings['lang'],
            'width': widget_settings['width'],
        }
        url_tpl = "{protocol}://{domain}{path}?lang={lang}&width={width}"
        return url_tpl.format(**url_ctx)


class ServeContentView(WidgetFactoryMixin):
    """ Serve locations content objects. Pass response to widget on client side.
    """
    def get(self, request, **kwargs):
        widget_settings = self.get_widget_settings()
        if translation.check_for_language(widget_settings['lang']):
            translation.activate(widget_settings['lang'])
        try:
            return render(request, self.get_template_name(),
                                   self.get_context_data())
        except TemplateDoesNotExist:
            raise Http404

    def get_context_data(self):
        protocol = 'https' if self.request.is_secure() else 'http'
        return {
            'object': self.object,
            'baseurl': "%s://%s" % (protocol, get_current_site(self.request), ),
        }

    def get_template_name(self):
        return 'locations/widgets/{}.html'.format(self.object._meta.model_name)


class WidgetFactory(WidgetFactoryMixin):
    """ Creates script that points to ServeContentView.
    """
    def get(self, request, **kwargs):
        widget_settings = self.get_widget_settings()
        f = open(os.path.join(settings.BASE_DIR, 'locations/scripts/widget-src.js'))
        contents = f.read().replace('{url}', self.create_url())
        contents = contents.replace('{width}', widget_settings['width'])
        contents = contents.replace('{div_id}', widget_settings['div_id'])
        return HttpResponse(contents, content_type="application/javascript")


class WidgetPreview(WidgetFactoryMixin):
    """ Show preview along with link to embed widget on client site.
    """
    template_name = 'locations/widget_preview.html'

    def get(self, request, **kwargs):
        widget_settings = self.get_widget_settings()
        path = reverse('locations:get-widget', kwargs={
            'ct': widget_settings['ct'],
            'pk': widget_settings['pk'], })
        protocol = 'https' if request.is_secure() else 'http'
        url = "{}://{}{}?lang={}".format(
            protocol, Site.objects.get_current().domain, path,
            translation.get_language_from_request(request))
        context = {
            'frame_src': self.create_url(),
            'div_id': "civil-widget-{}{}".format(
                widget_settings['ct'], widget_settings['pk']),
            'link': url, }
        return render(request, self.template_name, context)
