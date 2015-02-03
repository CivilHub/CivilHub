# -*- coding: utf-8 -*-
import os, json, codecs

from django.conf import settings

DIR = os.path.join(settings.BASE_DIR, 'dump')


def serialize_item(model):
    """ Zamienia wartości pól modelu na zserializowane wartości. Przyjmuje
    konkretną instancję modelu jako argument i zwraca słownik. """
    model_dict = {}
    for key, val in model.__dict__.iteritems():
        if key.startswith('_'):
            continue
        elif type(model.__dict__[key]).__name__ == 'ImageFieldFile':
            model_dict.update({key: model.__dict__[key].path})
        elif type(model.__dict__[key]).__name__ == 'datetime':
            model_dict.update({key: model.__dict__[key].isoformat()})
        else:
            model_dict.update({key: model.serializable_value(key)})
    return model_dict


def serialize_models(model_class):
    """
    Serializuje wszystkie obiekty z danego modelu i zwraca dane w formacie
    json.
    """
    model_data = []
    for item in model_class.objects.all():
        model_data.append(serialize_item(item))
    return json.dumps(model_data)


def export_items(model_class):
    """ Eksportuje wszystkie obiekty powiązane z danym modelem (klasę obiektów
    należy przekazać jako parametr do funkcji) do uniwersalnej postaci JSON
    i zapisuje wyniki do pliku w odpowiednim folderze. """
    dirname = os.path.join(DIR, model_class.__module__.split('.')[0].lower())
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    filename = os.path.join(dirname, model_class.__name__.lower() + '.json')
    f = codecs.open(filename, 'w+', 'utf-8')
    f.write(serialize_models(model_class))
    f.close()


def load_ideas():
    """ Przykład zastosowania powyższych funkcji w przypadku idei. Ta funkcja
    jest napisana "na raz", w związku z czym bez poprawek nie zadziała. """
    from django.contrib.auth.models import User
    from locations.models import Location
    from ideas.models import Idea
    from .helpers import date_from_iso
    f = codecs.open(os.path.join(DIR, 'ideas' ,'idea.json'), 'r', 'utf-8')
    data = json.loads(f.read())
    for l in data:
        try:
            idea = Idea.objects.create(
                creator = User.objects.get(pk=l['creator_id']),
                location = Location.objects.get(pk=l['location_id']),
                name = l['name'],
                description = l['description'],
                status = l['status'],
                date_created = date_from_iso(l['date_created']),
                date_edited = date_from_iso(l['date_edited'])
            )
        except Exception as ex:
            print ex.message
