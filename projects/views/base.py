# -*- coding: utf-8 -*-
import json

from PIL import Image

from django.contrib import messages
from django.contrib.auth.views import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from actstream.actions import follow, unfollow
from actstream.models import Action

from gallery.forms import BackgroundForm
from gallery.image import handle_tmp_image
from ideas.models import Idea
from locations.mixins import LocationContextMixin, SearchableListMixin
from locations.models import Location
from maps.models import MapPointer
from places_core.mixins import LoginRequiredMixin
from userspace.models import UserProfile

from ..actions import finished_task, joined_to_project, \
                      joined_to_task, leaved_project
from ..forms import CreateProjectForm, TaskForm, TaskGroupForm, \
                    ProjectNGOForm, UpdateProjectForm
from ..models import Task, TaskGroup, SocialProject
from ..permissions import check_access
from .mixins import ProjectAccessMixin, ProjectContextMixin


@require_POST
@login_required
def set_element_order(request, content_type, object_id, direction):
    """ We set an order for groups or tasks. The ID type of the content,
    the ID of the object and the direction ('UP' or 'DOWN') need to
    be passed to the function.
    """
    model = ContentType.objects.get(pk=content_type).model_class()
    obj = model.objects.get(pk=object_id)
    if direction == 'UP':
        obj.up()
    else:
        obj.down()
    if hasattr(obj, 'get_absolute_url'):
        # Task
        redirect_url = obj.get_absolute_url()
    else:
        # Group of tasks
        redirect_url = obj.project.get_absolute_url()
    return redirect(redirect_url)


@require_POST
@login_required
def toggle_task_state(request, pk):
    """ We change the status of the task to finished/unfinished """
    task = get_object_or_404(Task, pk=pk)
    if task.is_done:
        task.is_done = False
        message = _(u"Task marked as undone")
    else:
        task.is_done = True
        message = _(u"Task marked as finished")
    task.save()
    finished_task(request.user, task)
    if request.is_ajax():
        context = json.dumps(
            {'success': True,
             'is_done': task.is_done,
             'message': message, })
        return HttpResponse(context, content_type="application/json")
    return redirect(task.get_absolute_url())


class JoinProjectView(LoginRequiredMixin, LocationContextMixin, View):
    """ Adding/removing the user from the project (as a whole). """

    def post(self, request, location_slug=None, slug=None):
        project = get_object_or_404(SocialProject, slug=slug)
        if project.participants.filter(pk=request.user.pk).exists():
            project.participants.remove(request.user)
            project.authors_group.authors.remove(request.user.author)
            for group in project.taskgroup_set.all():
                for task in group.task_set.all():
                    if task.participants.filter(pk=request.user.pk).exists():
                        task.participants.remove(request.user)
            message = _("You are no longer in this project")
            leaved_project(request.user, project)
            unfollow(request.user, project)
        else:
            project.participants.add(request.user)
            project.authors_group.authors.add(request.user.author)
            message = _("You have joined to this project")
            joined_to_project(request.user, project)
            follow(request.user, project, actor_only=False)
        if request.is_ajax():
            context = {'success': True, 'message': message, }
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse(
            'locations:project_details',
            kwargs={'location_slug': location_slug,
                    'slug': project.slug, }))


class JoinTaskView(LoginRequiredMixin, LocationContextMixin, View):
    """ Adding/removing users from a concrete task. """

    def post(self, request, location_slug=None, slug=None, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        if task.participants.filter(pk=request.user.pk).exists():
            task.participants.remove(request.user)
            message = _("You are no longer in this task")
        else:
            task.participants.add(request.user)
            if not task.group.project.participants.filter(
                pk=request.user.pk).exists():
                task.group.project.participants.add(request.user)
                task.group.project.authors_group.authors.add(
                    request.user.author)
                joined_to_project(request.user,
                                                  task.group.project)
                follow(request.user, task.group.project, actor_only=False)
            else:
                joined_to_task(request.user, task)
            message = _("You have joined this task")
        if request.is_ajax():
            context = {'success': True, 'message': message, }
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse('locations:task_details',
                                kwargs={
                                    'location_slug': location_slug,
                                    'slug': task.group.project.slug,
                                    'task_id': task.pk,
                                }))


class CreateTaskGroupView(ProjectContextMixin, CreateView):
    """ Creation of a new group of tasks. The view takes only POST. """
    model = TaskGroup
    form_class = TaskGroupForm

    def get_success_url(self):
        return self.object.project.get_absolute_url()

    def get_initial(self):
        initial = super(CreateTaskGroupView, self).get_initial()
        project_slug = self.kwargs.get('slug')
        if project_slug is not None:
            initial.update({
                'project': get_object_or_404(SocialProject,
                                             slug=project_slug)
            })
        initial.update({'creator': self.request.user.pk})
        return initial


class UpdateTaskGroupView(ProjectAccessMixin, UpdateView):
    """ Edition of a group of tasks. """
    model = TaskGroup
    form_class = TaskGroupForm
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class DeleteTaskGroupView(ProjectAccessMixin, DeleteView):
    """ We remove a group of tasks. """
    model = TaskGroup
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class CreateTaskView(ProjectContextMixin, CreateView):
    """ Creation of a new task. """
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_initial(self):
        initial = super(CreateTaskView, self).get_initial()
        initial['creator'] = self.request.user
        group_id = self.kwargs.get('group_id')
        if group_id is not None:
            initial['group'] = get_object_or_404(TaskGroup, pk=group_id)
        return initial

    def form_valid(self, form):
        obj = form.save()
        obj.participants.add(obj.creator)
        obj.save()
        follow(obj.creator, obj.group.project, actor_only=False)
        return super(CreateTaskView, self).form_valid(form)


class UpdateTaskView(ProjectAccessMixin, UpdateView):
    """ Edition of existing elements. """
    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'task_id'


class DeleteTaskView(ProjectAccessMixin, DeleteView):
    """ We remove tasks. """
    model = Task
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return self.object.group.project.get_absolute_url()


class ProjectListView(LocationContextMixin, SearchableListMixin, ListView):
    """ A list of projects in one location. """
    model = SocialProject


class CreateProjectView(LoginRequiredMixin, LocationContextMixin, CreateView):
    """ New project creation for logged-in users. """
    model = SocialProject
    form_class = CreateProjectForm

    def get_context_data(self, form=None):
        context = super(CreateProjectView, self).get_context_data()
        context['form'] = form
        return context

    def get_initial(self):
        initial = super(CreateProjectView, self).get_initial()
        location_slug = self.kwargs.get('location_slug')
        if location_slug is not None:
            initial['location'] = get_object_or_404(Location,
                                                    slug=location_slug)
        idea_pk = self.kwargs.get('idea_pk')
        if idea_pk is not None:
            idea = get_object_or_404(Idea, pk=idea_pk)
            initial['idea'] = idea
            initial['location'] = idea.location
        initial['creator'] = self.request.user.pk
        return initial

    def form_valid(self, form):
        obj = form.save()

        # Fill in additional many 2 many fields and author entry
        obj.participants.add(obj.creator)
        obj.authors_group.authors.add(obj.creator.author)
        obj.save()

        # Start following for author - this way he will be noticed about
        # activities related to this project.
        follow(obj.creator, obj, actor_only=False, send_action=False)

        # Change project's idea status, if there is some related object
        if obj.idea is not None:
            obj.idea.status = 4
            obj.idea.save()

        # Create markers for map view
        try:
            for m in json.loads(self.request.POST.get('markers')):
                marker = MapPointer.objects.create(
                    content_type=ContentType.objects.get_for_model(
                        SocialProject),
                    object_pk=obj.pk,
                    latitude=m['lat'],
                    longitude=m['lng'])
        except Exception:
            # FIXME: silent fail, should be a flash message
            pass

        return super(CreateProjectView, self).form_valid(form)


class ProjectUpdateView(ProjectAccessMixin, UpdateView):
    """ Existing projects edition - only the creators and mods. """
    model = SocialProject
    form_class = UpdateProjectForm
    template_name = 'projects/socialproject_update.html'


class ProjectSummaryView(ProjectContextMixin, DetailView):
    """ A summary of key information about the project."""
    model = SocialProject
    template_name = 'projects/socialproject_summary.html'

    def get_context_data(self, object=None):
        context = super(ProjectSummaryView, self).get_context_data()
        ct = ContentType.objects.get_for_model(self.model).pk
        context['actions'] = Action.objects.filter(target_content_type_id=ct)\
                               .filter(target_object_id=self.get_object().pk)\
                               .order_by('-timestamp')
        return context


class ProjectParticipantsView(LocationContextMixin, ListView):
    """ Project participants list. """
    model = UserProfile
    template_name = 'projects/socialproject_participants.html'
    paginate_by = 24
    project_slug = None

    def get_queryset(self):
        self.project_slug = self.kwargs.get('slug')
        project = get_object_or_404(SocialProject, slug=self.project_slug)
        return project.participants.all()

    def get_context_data(self):
        context = super(ProjectParticipantsView, self).get_context_data()
        context['object'] = get_object_or_404(SocialProject,
                                              slug=self.project_slug)
        return context


class ProjectDetailView(ProjectContextMixin, DetailView):
    """ Tasks summary page within a project. """
    model = SocialProject

    def get_context_data(self, object=None):
        context = super(ProjectDetailView, self).get_context_data()
        task_id = self.kwargs.get('task_id')
        if task_id is not None:
            context['active_task'] = get_object_or_404(Task, pk=task_id)
        else:
            try:
                context['active_task'] = self.get_object()\
                                        .taskgroup_set.first().task_set.first()
            except AttributeError:
                # No tasks within this project
                pass
        return context


class ProjectBackgroundView(ProjectAccessMixin, FormView):
    """ Background image change for the whole project. """
    form_class = BackgroundForm
    template_name = 'projects/socialproject_background.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(SocialProject, slug=slug)

    def get_context_data(self, form=None):
        context = super(ProjectBackgroundView, self).get_context_data()
        if form is not None:
            context['form'] = form
        context['object'] = self.get_object()
        context['location'] = self.get_object().location
        return context

    def form_valid(self, form):
        box = (form.cleaned_data['x'], form.cleaned_data['y'],
               form.cleaned_data['x2'], form.cleaned_data['y2'], )
        obj = self.get_object()
        image = Image.open(form.cleaned_data['image'])
        image = image.crop(box)
        obj.image = handle_tmp_image(image)
        obj.save()
        return redirect(reverse(
            'locations:project_details',
            kwargs={'location_slug': obj.location.slug,
                    'slug': obj.slug, }))


class AddProjectToNGO(LoginRequiredMixin, View):
    """
    Allows users that joined to some organizations to add this project for
    NGO's project list.
    """
    template_name = 'projects/organization_add.html'
    form_class = ProjectNGOForm
    object = None

    def get_object(self, **kwargs):
        if self.object is None:
            project_slug = self.kwargs.get('project_slug')
            self.object = get_object_or_404(SocialProject, slug=project_slug)
        return self.object

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return {
            'object': self.object,
            'location': self.object.location,
            'project_access': check_access(self.object, self.request.user),
        }

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        initial = {'project': self.object, }
        context['form'] = self.form_class(initial=initial, request=request)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = self.form_class(request.POST, request=request)
        if not form.is_valid():
            context['form'] = form
            return render(request, self.template_name, context)
        obj = form.save()
        msg = _(u"Your organization was added to project mentors")
        messages.add_message(request, messages.SUCCESS, msg)
        return redirect(reverse('organizations:project-list',
                                kwargs={'slug': obj.slug, }))
