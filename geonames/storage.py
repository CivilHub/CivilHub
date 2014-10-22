import os, time
from django.conf import settings
from .models import *

DATA_PATH = os.path.join(settings.BASE_DIR, 'data')


def import_country(entry):
    """ Function takes one line of file and creates Country model. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # Incomplete entries are not desired
    if not entry[16] or entry[16] == ' ': return False
    
    country = CountryInfo.objects.create(
        id          = int(entry[16]),
        iso_alpha2  = entry[0],
        iso_alpha3  = entry[1],
        iso_numeric = entry[2],
        code        = entry[3],
        name        = entry[4],
        capital     = entry[5],
        area        = float(entry[6]) if entry[6] else 0.0,
        population  = int(entry[7]) if entry[7] else 0,
        continent   = entry[8],
        languages   = entry[15]
    )
    
    country.save()


def import_geoname(entry):
    """ Function takes single line of input file and creates GeoName instance. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # Incomplete entries are not desired
    if not entry[0] or entry[0] == ' ': return False
    
    geoname = GeoName.objects.create(
        id        = int(entry[0]),
        name      = entry[1],
        name_std  = entry[2],
        latitude  = float(entry[4]) if entry[4] else 0.0,
        longitude = float(entry[5]) if entry[4] else 0.0,
        feature_class = entry[6],
        feature_code  = entry[7],
        country = entry[8],
        admin1  = int(entry[10]) if entry[10] else 0,
        admin2  = int(entry[11]) if entry[11] else 0,
        admin3  = int(entry[12]) if entry[12] else 0,
        admin4  = int(entry[13]) if entry[13] else 0,
        population = int(entry[14]) if entry[14] else 0,
        timezone   = entry[17]
    )
    
    geoname.save()


def import_admin_code(entry):
    """ Function takes single line from admin1CodesASCII.txt file and creates
    admin code model in database. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # Incomplete entries are not desired
    if not entry[0] or entry[0] == ' ': return False
    
    admcode = AdminCode.objects.create(
        id       = int(entry[3]),
        name     = entry[1],
        name_std = entry[2],
        country  = entry[0].split('.')[0],
        code     = entry[0].split('.')[1]
    )
    
    admcode.save()


def import_alt_name(entry):
    """ Takes one line of input file and returns dictionary. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # We're interested only in 1st group langs
    if len(entry[2]) != 2: return None
    
    alt_name = AltName.objects.create(
        id           = int(entry[0]),
        geobaseid    = int(entry[1]),
        language     = entry[2],
        name         = entry[3],
        is_preferred = bool(entry[4]),
        is_short     = bool(entry[5]),
        is_historic  = bool(entry[6]),
        is_coloquial = bool(entry[7]),
    )
    
    alt_name.save()
