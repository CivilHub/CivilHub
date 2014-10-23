# -*- coding: utf-8 -*-
import os, time
from django.conf import settings
from cities.models import City

def read_entry(entry):
    """ Function takes single line from file and creates dict of values. """
    entry = entry.split('\t')
    try:
        mod_date = time.strptime(entry[18], "%Y-%m-%d")
    except ValueError:
        # improper or empty date
        mod_date = ''
    return {
        'geonameid'        : entry[0],
        'name'             : entry[1],
        'asciiname'        : entry[2],
        'alternatenames'   : entry[3],
        'latitude'         : entry[4],
        'longitude'        : entry[5],
        'feature_class'    : entry[6],
        'feature_code'     : entry[7],
        'country_code'     : entry[8],
        'cc2'              : entry[9],
        'admin1_code'      : entry[10],
        'admin2_code'      : entry[11],
        'admin3_code'      : entry[12],
        'admin4_code'      : entry[13],
        'population'       : entry[14],
        'elevation'        : entry[15],
        'dem'              : entry[16],
        'timezone'         : entry[17],
        'modification_date': mod_date,
    }

def check_city_data(country_code):
    """ Function takes single country file and performs comparison. Provide
    country code as argument - this is mandatory. In fact it does not work as
    it's suppose to. """
    errors = []
    city_count = 0
    country_code = str(country_code).upper() + '.txt'
    with open(os.path.join(settings.BASE_DIR, 'geobase', 'data', country_code)) as f:
        for entry in f:
            entry = read_entry(entry)
            city = None
            c = City.objects.filter(name=entry['name'], country__code=entry['country_code'])
            for cc in c:
                lng, lat = cc.location.get_coords()
                if lng == entry['longitude'] and lat == entry['latitude']:
                    city = cc
            if city is None:
                errors.append("Missing city: {}".format(entry['geonameid']))
            else:
                city_count += 1
    return city_count
