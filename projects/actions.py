# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action


def task_action(user, task, verb):
    """ Ogólna akcja związana z zadaniem. Składamy tutaj całe polecenie
    wysłania odpowiedniej akcji. Do funkcji należy przekazać instancję
    django.contrib.auth.models.User, projects.models.Task oraz verb. """
    action.send(user, verb=verb, action_object=task, target=task.group.project)


def finished_task(user, task):
    """ Użytkownik ukończył zadanie. """
    task_action(user, task, _(u"finished task"))


def joined_to_task(user, task):
    """ Użytkownik dołączył do zadania. """
    task_action(user, task, _(u"joined to task"))


def joined_to_project(user, project):
    """ Tej funkcji przekazujemy instancję django usera oraz projekt. """
    action.send(user, verb=_(u"joined to project"), target=project)

def leaved_project(user, project):
    """ J/w, ale tutaj informujemy innych, że użytkownik opuścił projekt. """
    action.send(user, verb=_(u"leaved project"), target=project)
