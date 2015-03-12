# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action


def project_created_action(sender, instance, created, **kwargs):
	""" Utworzenie projektu powinno być widoczne dla obserwatorów lokacji. """
	if created:
		action.send(instance.creator.user, verb=_(u"created"),
			action_object=instance, target=instance.location)


def project_task_action(sender, instance, created, **kwargs):
	"""
	Tworzenie grup i zadań powinno być widoczne tylko dla uczestników danego projektu.
	"""
	if created:
		if hasattr(instance, 'project'):
			# Utworzono grupę zadań
			action_target = instance.project
		else:
			# Utworzono zadanie
			action_target = instance.group.project
		action.send(instance.creator.user, verb=_(u"created"),
			action_object=instance, target=action_target)
