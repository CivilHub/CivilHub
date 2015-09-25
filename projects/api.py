# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets
from rest_framework.decorators import action, link
from rest_framework.response import Response

from .models import SocialProject, TaskGroup, Task
from .serializers import ProjectDetailSerializer, TaskSerializer, \
                         TaskGroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """ Base API endpoint for projects.

    Join/leave project
    ------------------
    <p>POST request to `/toggle/` API endpoint will add or remove current user
    from project's members. Returns updated info about that user is in project's
    member group or not.</p>
    <p>Example:</p>
    <pre class="prettyprint">var data = { csrfmiddlewaretoken: "the_token" };
    $.post('/api-projects/prjects/1/toggle/', data, function (r) {
      console.log(r); // {member: true}
    });</pre>

    Extra routes
    ------------
    `/api-projects/projects/1/groups/` - lists task groups for selected project.
    """
    model = SocialProject
    serializer_class = ProjectDetailSerializer

    @action()
    def toggle(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        if user.is_anonymous():
            raise PermissionDenied
        if user in obj.participants.all():
            obj.participants.remove(user)
            member = False
        else:
            obj.participants.add(user)
            member = True
        return Response({'member': member})

    @link()
    def groups(self, request, pk=None):
        obj = self.get_object()
        serializer = TaskGroupSerializer(obj.taskgroup_set.all(), many=True)
        return Response(serializer.data)


class TaskGroupViewSet(viewsets.ModelViewSet):
    """ Task groups.

    Extra routes
    ------------
    `/api-projects/groups/&lt;pk&gt/tasks/` - fetch list of all tasks belonging
    to selected group.
    """
    model = TaskGroup
    serializer_class = TaskGroupSerializer

    @link()
    def tasks(self, request, pk=None):
        obj = self.get_object()
        serializer = TaskSerializer(obj.task_set.all(), many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """ Tasks.

    Join/leave task
    ---------------
    <p>POST request to `/toggle/` API endpoint will add or remove current user
    from task's members. Returns updated info about that user is in task's
    member group or not.</p>
    <p>Example:</p>
    <pre class="prettyprint">var data = { csrfmiddlewaretoken: "the_token" };
    $.post('/api-projects/tasks/1/toggle/', data, function (r) {
      console.log(r); // {member: true}
    });</pre>
    """
    model = Task
    serializer_class = TaskSerializer

    @action()
    def toggle(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        if user.is_anonymous():
            raise PermissionDenied
        if user in obj.participants.all():
            obj.participants.remove(user)
            member = False
        else:
            obj.participants.add(user)
            member = True
        return Response({'member': member})

