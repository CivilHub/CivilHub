# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action


def task_action(user, task, verb):
    """
    A general action that contains tasks. Here we form whole send orders
    of a given action. A django.contrib.auth.models.User, projects.models.Task
    and verb instance needs to be passed to the function.
    """
    action.send(user, verb=verb, action_object=task, target=task.group.project)


def finished_task(user, task):
    """ The user has finished the task. """
    task_action(user, task, _(u"finished task"))


def joined_to_task(user, task):
    """ The user has joined the task."""
    task_action(user, task, _(u"joined to task"))


def joined_to_project(user, project):
    """ To this function we pass django user instance and project. """
    action.send(user, verb=_(u"joined to project"), target=project)


def leaved_project(user, project):
    """ Same as above but here we inform other poeple that the user has left the project. """
    action.send(user, verb=_(u"leaved project"), target=project)
