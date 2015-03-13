# -*- coding: utf-8 -*-
from places_core.permissions import is_moderator

def check_access(obj, user):
    """
    Funkcja sprawdza, czy dany użytkownik ma możliwość usuwania lub modyfikacji
    obiektu przekazanego jako argument. Obiektem musi być instancja modelu 
    z tej aplikacji, tzn projekt, grupa zadań lub zadanie. Zwraca True/False.
    """
    if user.is_anonymous:
        return False
    # "Twórca" zawsze może usunąć swoje "dzieło"
    access = user.profile == obj.creator
    # Superadmin może wszystko
    if not access and user.is_superuser:
        access = True
    # Sprawdzamy prawa moderatora
    if not access:
        location = None
        if hasattr(obj, 'location'):
            # Projekt
            location = obj.location
        elif hasattr(obj, 'project'):
            # Grupa zadań
            location = obj.project.location
        else:
            # Zadanie
            location = obj.group.project.location
        if is_moderator(user, location):
            access = True
    return access