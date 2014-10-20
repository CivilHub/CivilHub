# -*- coding: utf-8 -*-
import os
from django.conf import settings
from cities.models import Country, Region, Subregion, District, \
                           City, AlternativeName

FILE_PATH = os.path.join(settings.BASE_DIR, 'geobase', 'data', 'alternateNames.txt')

def decode_entry(entry):
    """ Takes one line of input file and returns dictionary. """
    entry = entry.split('\t')
    # We're interested only in 1st group langs
    if len(entry[2]) != 2: return None
    return {
        'id'          : int(entry[0]),
        'geobaseid'   : int(entry[1]),
        'language'    : entry[2],
        'name'        : entry[3],
        'is_preferred': bool(entry[4]),
        'is_short'    : bool(entry[5]),
        'is_historic' : bool(entry[6]),
        'is_coloquial': bool(entry[7]),
    }

def create_name_entry(name_data):
    """ Takes decoded dictionary and creates AlternativeName obj. """
    try:
        obj = Country.objects.get(pk=name_data['geobaseid'])
    except Country.DoesNotExist:
        obj = None
    if obj is None:
        try:
            obj = Region.objects.get(pk=name_data['geobaseid'])
        except Region.DoesNotExist:
            obj = None
    if obj is None:
        try:
            obj = Subregion.objects.get(pk=name_data['geobaseid'])
        except Subregion.DoesNotExist:
            obj = None
    if obj is None:
        try:
            obj = District.objects.get(pk=name_data['geobaseid'])
        except District.DoesNotExist:
            obj = None
    if obj is None:
        try:
            obj = City.objects.get(pk=name_data['geobaseid'])
        except City.DoesNotExist:
            obj = None

    if obj is not None:
        alt_name = AlternativeName.objects.create(
            id = name_data['id'],
            name = name_data['name'],
            language = name_data['language'],
            is_preferred = name_data['is_preferred'],
            is_short = name_data['is_short'],
            is_colloquial = name_data['is_coloquial']
        )
        obj.alt_names.add(alt_name)

def import_names():
    """ Reads file with alt names and creates proper objects. """
    with open(FILE_PATH) as f:
        for line in f:
            ndata = decode_entry(line)
            if ndata is not None:
                create_name_entry(ndata)

