# -*- coding: utf-8 -*-
import json
from PIL import Image

from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.views import login_required
from django.contrib.contenttypes.models import ContentType

from actstream.models import Action
from actstream.actions import follow, unfollow

from etherpad.forms import ServePadForm
from etherpad.models import Pad
from locations.mixins import LocationContextMixin
from locations.models import Location
from userspace.models import UserProfile
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from maps.models import MapPointer
from gallery.forms import BackgroundForm
from gallery.image import handle_tmp_image

import actions as project_actions
from .permissions import check_access
from .models import SocialProject, TaskGroup, Task, SocialForumTopic, SocialForumEntry
from .forms import CreateProjectForm, UpdateProjectForm, TaskGroupForm, TaskForm, \
                   DiscussionAnswerForm, SocialForumCreateForm, SocialForumUpdateForm, \
                   DocumentForm


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
    project_actions.finished_task(request.user, task)
    if request.is_ajax():
        context = json.dumps({
            'success': True,
            'is_done': task.is_done,
            'message': message,
        })
        return HttpResponse(context, content_type="application/json")
    return redirect(task.get_absolute_url())


class ProjectContextMixin(LocationContextMixin):
    """ A mixin for forms that create tasks and groups of tasks. """
    def get_context_data(self, form=None):
        group_id = self.kwargs.get('group_id')
        project_slug = self.kwargs.get('slug')
        location_slug = self.kwargs.get('location_slug')
        context = super(ProjectContextMixin, self).get_context_data(form)
        context['form'] = form
        if project_slug is not None:
            context['object'] = get_object_or_404(SocialProject, slug=project_slug)
            context['project_access'] = check_access(context['object'], self.request.user)
        if location_slug is not None:
            context['location'] = get_object_or_404(Location, slug=location_slug)
        return context


class ProjectAccessMixin(LoginRequiredMixin, ProjectContextMixin):
    """ We check whether the user has the proper access rights. """
    def get(self, request, location_slug=None, slug=None, group_id=None, task_id=None):
        # TODO: We can show something more appropriate than 403.
        if not check_access(self.get_object(), request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).get(request)

    def post(self, request, slug=None, location_slug=None, group_id=None, task_id=None):
        if not check_access(self.get_object(), request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).post(request)


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
            project_actions.leaved_project(request.user, project)
            unfollow(request.user, project)
        else:
            project.participants.add(request.user)
            project.authors_group.authors.add(request.user.author)
            message = _("You have joined to this project")
            project_actions.joined_to_project(request.user, project)
            follow(request.user, project, actor_only=False)
        if request.is_ajax():
            context = {'success': True, 'message': message,}
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse('locations:project_details', kwargs={
            'location_slug': location_slug,
            'slug': project.slug,
        }))


class JoinTaskView(LoginRequiredMixin, LocationContextMixin, View):
    """ Adding/removing users from a concrete task. """
    def post(self, request, location_slug=None, slug=None, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        if task.participants.filter(pk=request.user.pk).exists():
            task.participants.remove(request.user)
            message = _("You are no longer in this task")
        else:
            task.participants.add(request.user)
            if not task.group.project.participants.filter(pk=request.user.pk).exists():
                task.group.project.participants.add(request.user)
                task.group.project.authors_group.authors.add(request.user.author)
                project_actions.joined_to_project(request.user, task.group.project)
                follow(request.user, task.group.project, actor_only=False)
            else:
                project_actions.joined_to_task(request.user, task)
            message = _("You have joined this task")
        if request.is_ajax():
            context = {'success': True, 'message': message,}
            return HttpResponse(context, content_type="application/json")
        return redirect(reverse('locations:task_details', kwargs={
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
                'project': get_object_or_404(SocialProject, slug=project_slug)
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


class ProjectListView(LocationContextMixin, ListView):
    """ A list of projects in one location. """
    model = SocialProject

    def get_queryset(self):
        location_slug = self.kwargs.get('location_slug')
        if location_slug is None:
            return SocialProject.objects.all()
        return SocialProject.objects.filter(location__slug=location_slug)


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
            initial['location'] = get_object_or_404(Location, slug=location_slug)
        initial['creator'] = self.request.user.pk
        return initial

    def form_valid(self, form):
        obj = form.save()
        obj.participants.add(obj.creator)
        obj.authors_group.authors.add(obj.creator.author)
        obj.save()
        follow(obj.creator, obj, actor_only=False)
        try:
            for m in json.loads(self.request.POST.get('markers')):
                marker = MapPointer.objects.create(
                    content_type=ContentType.objects.get_for_model(SocialProject),
                    object_pk=obj.pk, latitude=m['lat'], longitude=m['lng'])
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
        context['object'] = get_object_or_404(SocialProject, slug=self.project_slug)
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


class ProjectDocumentsList(ListView):
    """ List all documents created for this project. """
    model = Pad
    paginate_by = 25

    def get_queryset(self):
        project = get_object_or_404(SocialProject, slug=self.kwargs.get('slug'))
        return self.model.objects.filter(group=project.authors_group)

    def get_context_data(self):
        context = super(ProjectDocumentsList, self).get_context_data()
        project = get_object_or_404(SocialProject, slug=self.kwargs.get('slug'))
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
        context['download_form'] = ServePadForm(initial={
            'pad': context['document'],
        })
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
        box = (
            form.cleaned_data['x'],
            form.cleaned_data['y'],
            form.cleaned_data['x2'],
            form.cleaned_data['y2'],
        )
        obj = self.get_object()
        image = Image.open(form.cleaned_data['image'])
        image = image.crop(box)
        obj.image = handle_tmp_image(image)
        obj.save()
        return redirect(reverse('locations:project_details',
            kwargs={
                'location_slug': obj.location.slug,
                'slug': obj.slug,
            }
        ))


class ProjectForumContextMixin(ProjectContextMixin):
    """ A mixin for discussion subpages for this project. """
    def get_context_data(self, form=None, **kwargs):
        context = super(ProjectForumContextMixin, self).get_context_data()
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            context['object'] = get_object_or_404(SocialProject, slug=project_slug)
            context['location'] = context['object'].location
            context['is_moderator'] = is_moderator(self.request.user, context['location'])
        if form is not None:
            context['form'] = form
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            context['discussion'] = get_object_or_404(SocialForumTopic, slug=discussion_slug)
        return context


class ProjectForumUpdateMixin(LoginRequiredMixin, UpdateView, ProjectForumContextMixin):
    """ A mixin for discussion edition forms and discussion entries. """
    def permission_check_(self):
        if not check_access(self.get_object(), self.request.user):
            raise PermissionDenied

    def get(self, request, project_slug=None, discussion_slug=None, pk=None):
        self.permission_check_()
        return super(ProjectForumUpdateMixin, self).get(request, project_slug, discussion_slug)

    def post(self, request, project_slug=None, discussion_slug=None, pk=None):
        self.permission_check_()
        return super(ProjectForumUpdateMixin, self).post(request, project_slug, discussion_slug)


class ProjectForumListView(ProjectForumContextMixin, ListView):
    """ A list of discussions within one project. """
    model = SocialForumTopic
    paginate_by = 25

    def get_queryset(self):
        qs = super(ProjectForumListView, self).get_queryset()
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            qs = qs.filter(project__slug=project_slug)
        return qs


class ProjectForumDetailView(ProjectForumContextMixin, ListView):
    """ One discussion with answers. """
    model = SocialForumEntry
    paginate_by = 25

    def get_queryset(self):
        qs = super(ProjectForumDetailView, self).get_queryset()
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            qs = qs.filter(topic__slug=discussion_slug)
        return qs

    def get_context_data(self):
        context = super(ProjectForumDetailView, self).get_context_data()
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            context['answer_form'] = DiscussionAnswerForm(initial={
                'topic': context['discussion'],
                'creator': self.request.user,
            })
            context['project_access'] = check_access(
                context['discussion'].project, self.request.user)
        return context


class ProjectForumCreateView(LoginRequiredMixin, CreateView, ProjectForumContextMixin):
    """ New discussion creation within a project. """
    model = SocialForumTopic
    form_class = SocialForumCreateForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            form.instance.project = get_object_or_404(SocialProject, slug=project_slug)
        return super(ProjectForumCreateView, self).form_valid(form)


class ProjectForumUpdateView(ProjectForumUpdateMixin):
    """ Existing discussion edition. """
    model = SocialForumTopic
    form_class = SocialForumUpdateForm
    slug_url_kwarg = 'discussion_slug'


class ProjectForumDeleteView(LoginRequiredMixin, DeleteView, ProjectForumContextMixin):
    """ Discussion deletion - only for admins and mods! """
    model = SocialForumTopic

    def get_success_url(self):
        return reverse('projects:discussions', kwargs={
            'project_slug': self.object.project.slug})

    def post(self, request, pk=None):
        if not is_moderator(request.user, self.get_object().project.location):
            raise PermissionDenied
        return super(ProjectForumDeleteView, self).post(request, pk)


class ProjectForumAnswerCreateView(LoginRequiredMixin, CreateView, ProjectForumContextMixin):
    """ Discussion answer. """
    model = SocialForumEntry
    form_class = DiscussionAnswerForm

    def get_success_url(self):
        return self.object.topic.get_absolute_url()

    def get_initial(self):
        initial = super(ProjectForumAnswerCreateView, self).get_initial()
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            initial['topic'] = get_object_or_404(SocialForumTopic, slug=discussion_slug)
        initial['creator'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ProjectForumAnswerCreateView, self).form_valid(form)


class ProjectForumAnswerUpdateView(ProjectForumUpdateMixin):
    """ Edition of your own discussion answers, possibly for admins. """
    model = SocialForumEntry
    form_class = DiscussionAnswerForm

    def get_success_url(self):
        return self.object.topic.get_absolute_url()


class ProjectForumAnswerDeleteView(LoginRequiredMixin, DeleteView, ProjectForumContextMixin):
    """ Discussion entries deletion - admins, mods and project owners. """
    model = SocialForumEntry

    def get_success_url(self):
        return self.object.topic.get_absolute_url()

    def post(self, request, pk=None):
        if not check_access(self.get_object().topic.project, request.user):
            raise PermissionDenied
        return super(ProjectForumAnswerDeleteView, self).post(request, pk)
