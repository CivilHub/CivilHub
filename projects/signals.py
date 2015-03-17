# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action


def project_created_action(sender, instance, created, **kwargs):
	""" Utworzenie projektu powinno być widoczne dla obserwatorów lokacji. """
	if created:
		action.send(instance.creator, verb=_(u"created"),
			action_object=instance, target=instance.location)


def project_task_action(sender, instance, created, **kwargs):
	"""
	Tworzenie grup i zadań powinno być widoczne tylko dla uczestników danego projektu.
	Tutaj obsługujemy także tworzenie tematów i odpowiedzi na forum.
	"""
	if created:
		if hasattr(instance, 'project'):
			# Utworzono grupę zadań lub dyskusję
			action_target = instance.project
		elif hasattr(instance, 'group'):
			# Utworzono zadanie
			action_target = instance.group.project
		else:
			# Utworzono odpowiedź do dyskusji
			action_target = instance.topic.project
		action.send(instance.creator, verb=_(u"created"),
			action_object=instance, target=action_target)
