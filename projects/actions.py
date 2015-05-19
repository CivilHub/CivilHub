# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action

from notifications.models import notify


def task_action(user, task, verb):
    """
    A general action that contains tasks. Here we form whole send orders
    of a given action. A django.contrib.auth.models.User, projects.models.Task
    and verb instance needs to be passed to the function.
    """
    action.send(user, verb=verb, action_object=task, target=task.group.project)


def finished_task(user, task):
    """
    The user has finished the task.
    """
    task_action(user, task, _(u"finished task"))
    for participant in task.participants.all():
        notify(user, participant,
            verb=_(u"finished task"),
            key="project",
            action_tartget=task
        )


def joined_to_task(user, task):
    """
    The user has joined the task.
    """
    if user != task.creator:
        task_action(user, task, _(u"joined to task"))
        notify(user, task.creator,
            verb=_(u"joined to your task"),
            key="follower",
            action_target=task
        )


def joined_to_project(user, project):
    """
    To this function we pass django user instance and project.
    """
    if user != project.creator:
        action.send(user, verb=_(u"joined to project"), target=project)
        notify(user, project.creator,
            verb=_(u"joined to your project"),
            key="follower",
            action_target=project
        )


def leaved_project(user, project):
    """
    Same as above but here we inform other poeple that the user has left the project.
    """
    action.send(user, verb=_(u"leaved project"), target=project)
