# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormView, UpdateView

from actstream.actions import follow

from civmail.messages import InviteToOrganization
from locations.models import Location
from places_core.helpers import ct_for_obj
from places_core.mixins import LoginRequiredMixin
from simpleblog.forms import BlogEntryForm
from simpleblog.models import BlogEntry

from .forms import NGOInviteForm, \
                   OrganizationForm, \
                   OrganizationLocationForm, \
                   NGOBackgroundForm, \
                   NGOProjectForm, \
                   NGOSearchForm
from .models import Category, Invitation, Organization


class NGOContextMixin(SingleObjectMixin):
    """
    Provides common context variables used across NGO subpages.
    """
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(NGOContextMixin, self).get_context_data(**kwargs)
        context['organization'] = self.object
        context['access'] = self.object.has_access(self.request.user)
        context['member'] = self.request.user in self.object.users.all()
        return context


class OrganizationListView(ListView):
    """ Presents list of all registered organizations.
    """
    model = Organization
    paginate_by = 25
    form_class = NGOSearchForm

    def get_form(self):
        self.form =  self.form_class(self.request.GET)
        return self.form

    def get_queryset(self):
        qs = super(OrganizationListView, self).get_queryset()
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data.get('name')
            country = form.cleaned_data.get('country')
            location = form.cleaned_data.get('location')
            kind = form.cleaned_data.get('kind')
        if name:
            qs = qs.filter(name__icontains=name)
        if location:
            locations = Location.objects.filter(name__icontains=location)
            qs = qs.filter(locations__in=locations)
        elif country is not None:
            locations = Location.objects.filter(country_code=country.country_code)
            qs = qs.filter(locations__in=locations)
        if kind is not None:
            qs = qs.filter(category=kind)
        return qs.order_by('name').distinct()

    def get_context_data(self):
        context = super(OrganizationListView, self).get_context_data()
        context['countries'] = Location.objects.filter(kind='country')
        context['categories'] = Category.objects.all()
        context['form'] = self.form
        return context


class OrganizationView(DetailView):
    """
    Main page for organization.
    """
    model = Organization
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = super(OrganizationView, self).get_context_data(**kwargs)
        context['access'] = self.object.has_access(self.request.user)
        context['member'] = self.request.user in self.object.users.all()
        return context


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    """
    Registered users may create new organizations.
    """
    model = Organization
    form_class = OrganizationForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        form.save_m2m()
        obj.users.add(self.request.user)
        follow(self.request.user, obj)
        return super(OrganizationCreateView, self).form_valid(form)


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    """
    Users with access rights can edit existing organizations.
    """
    model = Organization
    form_class = OrganizationForm
    context_object_name = 'organization'
    template_name = 'organizations/organization_update.html'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(OrganizationUpdateView, self).dispatch(*args, **kwargs)


class OrganizationLocationList(DetailView):
    """
    Presents entire list of organizations locations.
    """
    model = Organization
    template_name = 'organizations/location_list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(OrganizationLocationList,
                        self).get_context_data(**kwargs)
        context['object_list'] = self.object.locations.all()
        context['access'] = self.object.has_access(self.request.user)
        return context


class OrganizationLocationAdd(LoginRequiredMixin, NGOContextMixin, FormView):
    """
    Add new location to organization's locations list.
    """
    model = Organization
    template_name = 'organizations/location_add.html'
    form_class = OrganizationLocationForm
    context_object_name = 'organization'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(OrganizationLocationAdd, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        for location in form.cleaned_data['locations']:
            if not location in self.object.locations.all():
                self.object.locations.add(location)
        return super(OrganizationLocationAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse('organizations:locations',
                       kwargs={'slug': self.object.slug})


class OrganizationLocationDelete(NGOContextMixin, View):
    """
    Delete location from organizations locations list.
    """
    model = Organization

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(OrganizationLocationDelete, self).dispatch(*args, **kwargs)

    def get(self, request, slug=None):
        raise Http404

    def post(self, request, slug=None):
        location = Location.objects.get(
            pk=int(self.request.POST.get('location_id')))
        if location in self.object.locations.all():
            self.object.locations.remove(location)
            self.object.save()
        return redirect(reverse('organizations:locations',
                                kwargs={'slug': self.object.slug}))


class OrganizationMemberList(ListView):
    """
    List all users that are members of this organization.
    """
    model = User
    template_name = 'organizations/member_list.html'
    paginate_by = 25
    organization = None

    def dispatch(self, *args, **kwargs):
        self.organization = get_object_or_404(Organization,
                                              slug=self.kwargs.get('slug'))
        return super(OrganizationMemberList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.organization.users.all()

    def get_context_data(self, **kwargs):
        context = super(OrganizationMemberList, self).get_context_data(**kwargs)
        context['organization'] = self.organization
        context['access'] = self.organization.has_access(self.request.user)
        return context


class OrganizationMemberDelete(SingleObjectMixin, View):
    """
    View to handle POST request when we want to remove user from organization.
    """
    model = Organization

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(OrganizationMemberDelete, self).dispatch(*args, **kwargs)

    def get(self, request, slug=None):
        raise Http404

    def post(self, request, slug=None):
        user = User.objects.get(pk=int(self.request.POST.get('user_id')))
        if user in self.object.users.all():
            self.object.users.remove(user)
            self.object.save()
            for i in Invitation.objects.filter(user=user,
                                               organization=self.object):
                i.delete()
        return redirect(reverse('organizations:members',
                                kwargs={'slug': self.object.slug}))


class InviteUsers(NGOContextMixin, FormView):
    """
    Invite others to this organization by sending them email.
    """
    model = Organization
    form_class = NGOInviteForm
    template_name = 'organizations/member_invite.html'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise Http404
        return super(InviteUsers, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(InviteUsers, self).get_initial()
        initial['organization'] = self.get_object()
        return initial

    def form_valid(self, form):
        for user in form.users:
            invitation, created = Invitation.objects.get_or_create(
                organization=self.object,
                user=user)
            message = InviteToOrganization()
            msg_context = {
                'lang': user.profile.lang,
                'user': self.object.creator,
                'organization': self.object,
                'link': self.request.build_absolute_uri(
                    reverse('organizations:accept',
                            kwargs={'key': invitation.key}))
            }
            if created:
                message.send(user.email, msg_context)
        messages.add_message(self.request, messages.SUCCESS,
                             _(u"All messages sent"))
        return super(InviteUsers, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class InviteAcceptView(LoginRequiredMixin, DetailView):
    """
    Accept invitation passing it's code to check if it's still valid.
    """
    model = Invitation
    slug_field = 'key'
    slug_url_kwarg = 'key'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_accepted or self.request.user != self.object.user:
            raise Http404
        return super(InviteAcceptView, self).dispatch(*args, **kwargs)

    def get(self, request, key=None):
        self.object = self.get_object()
        self.object.accept()
        messages.add_message(request, messages.SUCCESS,
                             _(u"You have accepted invitation"))
        return redirect(self.object.organization.get_absolute_url())


class NGONewsCreate(LoginRequiredMixin, NGOContextMixin, View):
    """
    Users that are members of organization may publish contents on this page.
    """
    form_class = BlogEntryForm
    template_name = 'organizations/news_form.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super(NGONewsCreate, self).get_context_data(**kwargs)
        context['form'] = self.form_class(initial={
            'content_type': ct_for_obj(self.object),
            'object_id': self.object.pk,
        })
        return render(request, self.template_name, context)


class NGONewsList(NGOContextMixin, View):
    """
    Present list of all news items made in this NGO.
    """
    template_name = 'organizations/news_list.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super(NGONewsList, self).get_context_data(**kwargs)
        context['object_list'] = BlogEntry.objects.get_published_in(self.object)
        return render(request, self.template_name, context)


class NGONewsDetail(NGOContextMixin, View):
    """
    Show detailed page for simpleblog entry for this organization.
    """
    template_name = 'organizations/news_detail.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super(NGONewsDetail, self).get_context_data(**kwargs)
        context['news'] = get_object_or_404(BlogEntry,
                                            slug=self.kwargs.get('news_slug'))
        return render(request, self.template_name, context)


class NGOBackgroundView(NGOContextMixin, View):
    """
    A static form that allows to upload and crop background images for organizations.
    """
    template_name = 'organizations/organization_background.html'
    form_class = NGOBackgroundForm

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super(NGOBackgroundView, self).get_context_data()
        context['form'] = self.form_class(
            initial={'organization': self.object, })
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form, })
        ngo = form.cleaned_data['organization']
        return redirect(ngo.get_absolute_url())


class NGOProjectList(NGOContextMixin, View):
    """
    Nanages list of projects where given organization is a mentor.
    """
    template_name = 'organizations/socialproject_list.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super(NGOProjectList, self).get_context_data()
        context['object_list'] = self.object.projects.all()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        user = request.user
        if user.is_anonymous() or not self.object.has_access(user):
            raise PermissionDenied
        try:
            project_id = int(request.POST.get('project_id'))
        except (TypeError, ValueError):
            raise Http404
        try:
            project = self.object.projects.get(pk=project_id)
        except ObjectDoesNotExist:
            raise Http404
        self.object.projects.remove(project)
        msg = _(u"Project has been removed from organizations list")
        messages.add_message(request, messages.SUCCESS, msg)
        return redirect(reverse('organizations:project-list',
                                kwargs={'slug': self.object.slug, }))


class NGOProjectAdd(LoginRequiredMixin, NGOContextMixin, View):
    """
    Authorized users may add new projects to NGO's project list.
    """
    template_name = 'organizations/socialproject_form.html'
    form_class = NGOProjectForm

    def get(self, request, **kwargs):
        self.object = self.get_object()
        user = request.user
        if not self.object.has_access(user):
            raise Http404
        context = super(NGOProjectAdd, self).get_context_data()
        context['form'] = self.form_class(instance=self.object)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if not form.is_valid():
            context = super(NGOProjectAdd, self).get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        obj = form.save(commit=False)
        form.save_m2m()
        return redirect(reverse('organizations:project-list',
                                kwargs={'slug': self.object.slug, }))
