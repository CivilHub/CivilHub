# -*- coding: utf-8 -*-

# UWAGA: widoki, które są tutaj zdefiniowane, współpracują ściśle
# z aplikacją 'locations'. Ta aplikacja nie definiuje urli - korzystamy
# tutaj z lokalizacji. Widoki są zaprojektowane pod konkretny układ URL-i.

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

from locations.mixins import LocationContextMixin
from locations.models import Location
from userspace.models import UserProfile
from places_core.mixins import LoginRequiredMixin
from maps.models import MapPointer
from gallery.forms import BackgroundForm
from gallery.image import handle_tmp_image

import actions as project_actions
from .permissions import check_access
from .models import SocialProject, TaskGroup, Task, SocialForumTopic, SocialForumEntry
from .forms import CreateProjectForm, UpdateProjectForm, TaskGroupForm, TaskForm, \
                   DiscussionAnswerForm


@require_POST
@login_required
def set_element_order(request, content_type, object_id, direction):
    """ Ustawiamy porządek dla grup lub zadań. Do funkcji należy przekazać
    ID typu zawartości, ID obiektu oraz kierunek ('UP' lub 'DOWN'). """
    model = ContentType.objects.get(pk=content_type).model_class()
    obj = model.objects.get(pk=object_id)
    if direction == 'UP':
        obj.up()
    else:
        obj.down()
    if hasattr(obj, 'get_absolute_url'):
        # Zadanie
        redirect_url = obj.get_absolute_url()
    else:
        # Grupa zadań
        redirect_url = obj.project.get_absolute_url()
    return redirect(redirect_url)


@require_POST
@login_required
def toggle_task_state(request, pk):
    """ Zmieniamy stan zadania ukończony/nieukończony. """
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
    """ Mixin dla formularzy do tworzenia zadań oraz grup zadań. """
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
    """
    Sprawdzamy, czy użytkownik ma odpowiednie prawa dostępu.
    """
    def get(self, request, location_slug=None, slug=None, group_id=None, task_id=None):
        # TODO: można pokazać coś bardziej odpowiedniego niż 403.
        if not check_access(self.get_object(), request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).get(request)

    def post(self, request, slug=None, location_slug=None, group_id=None, task_id=None):
        if not check_access(self.get_object(), request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).post(request)


class JoinProjectView(LoginRequiredMixin, LocationContextMixin, View):
    """ Dołączanie/odłączanie użytkownika od całego projektu. """
    def post(self, request, location_slug=None, slug=None):
        project = get_object_or_404(SocialProject, slug=slug)
        if request.user in project.participants.all():
            project.participants.remove(request.user)
            for group in project.taskgroup_set.all():
                for task in group.task_set.all():
                    if request.user in task.participants.all():
                        task.participants.remove(request.user)
            message = _("You are no longer in this project")
            project_actions.leaved_project(request.user, project)
            unfollow(request.user, project)
        else:
            project.participants.add(request.user)
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
    """ Dołączanie/odłączanie użytkowników od konkretnego zadania. """
    def post(self, request, location_slug=None, slug=None, task_id=None):
        task = get_object_or_404(Task, pk=task_id)
        if request.user in task.participants.all():
            task.participants.remove(request.user)
            message = _("You are no longer in this task")
        else:
            task.participants.add(request.user)
            if not request.user in task.group.project.participants.all():
                task.group.project.participants.add(request.user)
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
    """ Tworzenie nowej grupy dla zadań. Widok przyjmuje tylko POST. """
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
    """ Edycja grupy dla zadań. """
    model = TaskGroup
    form_class = TaskGroupForm
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class DeleteTaskGroupView(ProjectAccessMixin, DeleteView):
    """ Usuwamy grupy zadań. """
    model = TaskGroup
    pk_url_kwarg = 'group_id'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class CreateTaskView(ProjectContextMixin, CreateView):
    """ Tworzenie nowego zadania. """
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
    """ Edycja istniejących zadań. """
    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'task_id'


class DeleteTaskView(ProjectAccessMixin, DeleteView):
    """ Usuwamy zadania. """
    model = Task
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return self.object.group.project.get_absolute_url()


class ProjectListView(LocationContextMixin, ListView):
    """ Lista projektów w ramach jednej lokalizacji. """
    model = SocialProject

    def get_queryset(self):
        location_slug = self.kwargs.get('location_slug')
        if location_slug is None:
            return SocialProject.objects.all()
        return SocialProject.objects.filter(location__slug=location_slug)


class CreateProjectView(LoginRequiredMixin, LocationContextMixin, CreateView):
    """ Tworzenie nowego projektu dla zalogowanych użytkowników. """
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
        obj.save()
        follow(obj.creator, obj, actor_only=False)
        try:
            for m in json.loads(self.request.POST.get('markers')):
                marker = MapPointer.objects.create(
                    content_type=ContentType.objects.get_for_model(SocialProject),
                    object_pk=obj.pk, latitude=m['lat'], longitude=m['lng'])
        except Exception:
            # FIXME: silent fail, powinna być flash message
            pass
        return super(CreateProjectView, self).form_valid(form)


class ProjectUpdateView(ProjectAccessMixin, UpdateView):
    """ Edycja istniejących projektów - tylko twórcy i moderatorzy. """
    model = SocialProject
    form_class = UpdateProjectForm
    template_name = 'projects/socialproject_update.html'


class ProjectSummaryView(ProjectContextMixin, DetailView):
    """ Podsumowanie najważniejszych informacji o projekcie. """
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
    """ Lista uczetników prjektu. """
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
    """ Strona podsumowania zadań w ramach projektu. """
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
                # Brak zadań w ramach tego projektu
                pass
        return context


class ProjectBackgroundView(ProjectAccessMixin, FormView):
    """ Zmiana tła dla całego projektu. """
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
    """ Mixin dla podstron z dyskusjami do projektu. """
    def get_context_data(self, form=None):
        context = super(ProjectForumContextMixin, self).get_context_data()
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            context['object'] = get_object_or_404(SocialProject, slug=project_slug)
            context['location'] = context['object'].location
        if form is not None:
            context['form'] = form
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            context['discussion'] = get_object_or_404(SocialForumTopic, slug=discussion_slug)
        return context


class ProjectForumListView(ProjectForumContextMixin, ListView):
    """ Lista dyskusji w ramach jednego projektu. """
    model = SocialForumTopic
    paginate_by = 25

    def get_queryset(self):
        qs = super(ProjectForumListView, self).get_queryset()
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            qs = qs.filter(project__slug=project_slug)
        return qs


class ProjectForumDetailView(ProjectForumContextMixin, ListView):
    """ Jedna dyskusja, wraz z odpowiedziami. """
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
        return context


class ProjectForumAnswerCreateView(LoginRequiredMixin, CreateView, ProjectForumContextMixin):
    """
    Odpowiadanie na dyskusję - GET jest tutaj tylko do celów testowych, decelowo
    formularz ma się znajdować przy liście wszystkich odpowiedzi, a tutaj
    obsługujemy tylko samo tworzenie nowego obiektu.
    """
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
