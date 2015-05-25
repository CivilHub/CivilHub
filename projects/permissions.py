# -*- coding: utf-8 -*-
from places_core.permissions import is_moderator

def check_access(obj, user):
    """
    This function checkes whether the user is allowed to delete or modify the
    object passed in as an argument. Such an object must be a model instance
    of this application. i.e. project, group of tasks or a task. Returns
    True/False.
    """
    if user.is_anonymous():
        return False
    # The "creator" can always delete his/her "work"
    access = user == obj.creator
    # The Superadmin is omnipotent
    if not access and user.is_superuser:
        access = True
    # We check the mods rights
    if not access:
        location = None
        if hasattr(obj, 'location'):
            # Project
            location = obj.location
        elif hasattr(obj, 'project'):
            # A Group of taks or a topic in the forum
            location = obj.project.location
        elif hasattr(obj, 'group'):
            # Task
            location = obj.group.project.location
        else:
            # Entry in the forum
            location = obj.discussion.project.location
        if is_moderator(user, location):
            access = True
    return access
