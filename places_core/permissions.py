# -*- coding: utf-8 -*-
#
# Customowe uprawnienia dla użytkowników. Jeżeli zaistnieje
# taka potrzeba, skorzystamy z jakiejś paczki w rodzaju django-guardian.
#
from django.contrib.auth.models import User
from userspace.models import UserProfile


def is_moderator(user, location):
    """
    Funkcja sprawdza, czy użytkownik jest moderatorem
    w danej lokalizacji. Zwraca 'True' również dla
    superadminów.
    """
    if user.is_superuser:
        return True

    if user.is_anonymous:
        return False

    profile = UserProfile.objects.get(user = user)
    if location in profile.mod_areas.all():
        return True

    return False
