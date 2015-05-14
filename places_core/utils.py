# -*- coding: utf-8 -*-
import os, json, codecs

from django.conf import settings

DIR = os.path.join(settings.BASE_DIR, 'dump')


def get_current_version():
    """ Returns current PROJECT version. This is useful for static files builds,
        e.g. scripts and styles. This way we can append common suffx for all files
        as well as for HTML tags later.
    """
    try:
        v_file = open(os.path.join(settings.BASE_DIR, 'VERSION'))
    except IOError:
        return '0.0.0'
    version = v_file.read().strip()
    v_file.close()
    return version


def serialize_item(model):
    """ Changes the values of model fields on a serialized value. It takes
    a concrete instance of the model as an argument and returns a dictionary. """
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
    Serializes all objects from a given model and returns the data in json format.
    """
    model_data = []
    for item in model_class.objects.all():
        model_data.append(serialize_item(item))
    return json.dumps(model_data)


def export_items(model_class):
    """ Exports all objects connected with a given model (class objects need
    to be passed as a function parameter) to a universal JSON format and
    saves the results in a file in a proper folder. """
    dirname = os.path.join(DIR, model_class.__module__.split('.')[0].lower())
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    filename = os.path.join(dirname, model_class.__name__.lower() + '.json')
    f = codecs.open(filename, 'w+', 'utf-8')
    f.write(serialize_models(model_class))
    f.close()


def load_ideas():
    """ An example of a how the above function can be used in an idea. This
    function is written 'as once', therefore it will not work without
    corrections.
    """
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
