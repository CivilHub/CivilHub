# -*- coding: utf-8 -*-
#
# Customowe uprawnienia dla użytkowników. Jeżeli zaistnieje
# taka potrzeba, skorzystamy z jakiejś paczki w rodzaju django-guardian.
#
from django.contrib.auth.models import User, Group
from userspace.models import UserProfile


def is_moderator(user, location):
    """
    Funkcja sprawdza, czy użytkownik jest moderatorem
    w danej lokalizacji. Zwraca 'True' również dla
    superadminów i "supermoderatorów".
    """
    if user.is_superuser:
        return True

    # Nazwa grupy jest przypisana "na sztywno" !!!
    if 'Editor' in [x.name for x in Group.objects.all()]:
        return True

    if user.is_anonymous():
        return False

    profile = UserProfile.objects.get(user = user)
    if location in profile.mod_areas.all():
        return True

    return False