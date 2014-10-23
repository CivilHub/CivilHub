import os, time
from django.conf import settings
from .models import *

DATA_PATH = os.path.join(settings.BASE_DIR, 'data')

# set custom log because of problems with django-one:
import logging
logging.basicConfig(filename=os.path.join(settings.BASE_DIR, 'logs', 'django.log'),
                   level=logging.INFO)


def import_country(entry):
    """ Function takes one line of file and creates Country model. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # Incomplete entries are not desired
    if not entry[16] or entry[16] == ' ': return False
    
    try:
        chk = CountryInfo.objects.get(pk=int(entry[16]))
        # Entry exists. Skipping.
        logging.info("Country already exists: %s. Skipping",
                     unicode(entry[4]).encode('utf-8'))
        return True
    except CountryInfo.DoesNotExist:
        pass
    
    try:
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

        logging.info("Country saved: %s",
                     unicode(entry[4]).encode('utf-8'))
    except Exception as ex:
        logging.error("Error importing country: %s - %s",
                      unicode(entry[4]).encode('utf-8'), ex.strerror)


def import_geoname(entry):
    """ Function takes single line of input file and creates GeoName instance. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # Incomplete entries are not desired
    if not entry[0] or entry[0] == ' ': return False
    
    try:
        chk = GeoName.objects.get(pk=int(entry[0]))
        # Entry exists. Skipping.
        logging.info("GeoName object already exists: %s. Skipping", entry[0])
        return True
    except GeoName.DoesNotExist:
        pass
    
    try: 
        geoname = GeoName.objects.create(
            id        = int(entry[0]),
            name      = entry[1],
            name_std  = entry[2],
            latitude  = float(entry[4]) if entry[4] else 0.0,
            longitude = float(entry[5]) if entry[4] else 0.0,
            feature_class = entry[6],
            feature_code  = entry[7],
            country = entry[8],
            admin1  = entry[10],
            admin2  = entry[11],
            admin3  = entry[12],
            admin4  = entry[13],
            population = int(entry[14]) if entry[14] else 0,
        )
    
        geoname.save()
        
        logging.info("GeoName object saved: %s", unicode(entry[1]).encode('utf-8'))
    except Exception as ex:
        logging.error("Error importing GeoName: %s - %s", entry[0], repr(ex))


def import_admin_code(entry):
    """
    Function takes single line from admin1CodesASCII.txt file and creates
    admin code model in database.
    """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # Incomplete entries are not desired
    if not entry[0] or entry[0] == ' ': return False
    
    try:
        chk = AdminCode.objects.get(pk=int(entry[3]))
        # Entry exists. Skipping.
        logging.info("Admin code already exists: %s. Skipping",
                     entry[3].replace('\n', ''))
        return True
    except AdminCode.DoesNotExist:
        pass
    
    try:
        admcode = AdminCode.objects.create(
            id       = int(entry[3]),
            name     = entry[1],
            name_std = entry[2],
            country  = entry[0].split('.')[0],
            code     = entry[0].split('.')[1]
        )
        
        admcode.save()
        
        logging.info("Admin code object saved: %s", entry[3].replace('\n', ''))
    except Exception as ex:
        logging.error("Error importing Admin code: %s - %s",
                      entry[3].replace('\n', ''), repr(ex))


def import_alt_name(entry):
    """ Takes one line of input file and returns dictionary. """
    if entry.startswith('#'):
        return False
    entry = entry.split('\t')
    
    # We're interested only in 1st group langs
    if len(entry[2]) != 2: return None
    
    try:
        chk = AltName.objects.get(pk=int(entry[0]))
        # Entry exists. Skipping.
        logging.info("Alternate name already exists: %s. Skipping",
                     unicode(entry[3]).encode('utf-8'))
        return True
    except AltName.DoesNotExist:
        pass
    
    try:
        alt_name = AltName.objects.create(
            id            = int(entry[0]),
            geonameid     = int(entry[1]),
            language      = entry[2],
            altername     = unicode(entry[3]),
            is_preferred  = bool(entry[4]),
            is_short      = bool(entry[5]),
            is_historic   = bool(entry[6]),
            is_colloquial = bool(entry[7]),
        )
        
        alt_name.save()
        
        logging.info("Alternate name object saved: %s",
                             unicode(entry[3]).encode('utf-8'))
    except Exception as ex:
        logging.error("Error importing Alternate name: %s - %s",
                      unicode(entry[3]).encode('utf-8'), repr(ex))
