# -*- coding: utf-8 -*-
"""
Moduł zarządzający zrzutem danych z bazy do plików JSON. Pliki są posegregowane
na foldery państw odpowiadające modelom `country` w bazie.
"""
import os, json
from django.conf import settings
from maps.serializers import MapPointerSerializer
from maps.models import MapPointer
from locations.models import Location
from locations.serializers import MapLocationSerializer
from .models import Country


def country_codes():
    """
    Funkcja zwracająca nazwy państw w języku angielskim połączone z ich kodami
    ISO. Dane zczytywane są z pliku JSON i zwracane w formie listy słowników.
    """
    f = open(os.path.join(settings.BASE_DIR, 'geobase/data/codes.json'))
    codes = f.read()
    f.close()
    return json.loads(codes)


class CountryJSONStorage(object):
    """
    Klasa umożliwiająca import/export znaczników na mapie do postaci JSON-a
    i odwrotnie. Opiera się na serializerach znaczników wykorzystanych w REST
    api.
    
    TODO: Import danych nie jest jeszcze zaimplementowany.
    """
    def __init__(self, path=None):
        """
        W trakcie inicjalizacji możemy bezpośrednio nadpisać ustawienia
        z pliku `settings.py` projektu.
        Parametr `path` pozwala określić bezpośrednią ścieżkę do folderu.
        """
        self.path = path or settings.COUNTRY_STORAGE_PATH

    def save_file_(self, data, country_pk):
        """
        Funkcja, która zapisuje dane bezpośrednio do pliku. Najczęściej
        `country_pk` będzie odpowiadać ID obiektu Country, dla którego dumpujemy
        dane. Data to dane z serializera zdumpowane już do ciągu znaków.
        """
        filepath = os.path.join(self.path, str(country_pk))
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        f = open(os.path.join(filepath, 'markers.json'), 'w')
        f.write(json.dumps(data))
        f.close()
        print "File saved: ", os.path.join(filepath, 'markers.json')

    def load_file_(self, country_pk):
        """
        Metoda odczytująca plik JSON i zwracająca zserializowaną listę obiektów
        w formacie JSON.
        """
        f = open(os.path.join(self.path, str(country_pk), 'markers.json'))
        data = f.read()
        f.close()
        markers = json.loads(data)
        return markers

    def save_locations_(self, data, country_pk):
        """
        Zapisujemy sub-lokalizacje dla danego kraju, podobnie, jak robimy to
        z markerami. Dla lokalizacji zrobimy jednak osobny plik.
        """
        filepath = os.path.join(self.path, str(country_pk))
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        f = open(os.path.join(filepath, 'locations.json'), 'w')
        f.write(json.dumps(data))
        f.close()
        print "File saved: ", os.path.join(filepath, 'locations.json')

    def load_locations_(self, country_pk):
        """
        Podobnie jak w przypadku load_file_, ta metoda zwraca zawartość pliku
        JSON z zaznaczonymi lokacjami, które mają swoje miejsce na mapie (tzn
        posiadają określoną długość i szerokość geograficzną.
        """
        f = open(os.path.join(self.path, str(country_pk), 'locations.json'))
        data = f.read()
        locations = json.loads(data)
        return locations

    def get_markers(self, country):
        """
        Funkcja "zbiera" wszystkie markery dla danego kraju (country).
        """
        map_pointers = []
        for map_pointer in MapPointer.objects.all():
            print map_pointer
            if map_pointer.content_object.location.country_code == country.code:
                map_pointers.append(map_pointer)
        return map_pointers

    def dump_data(self, country_code=None, dump_locations=True, dump_markers=True):
        """
        Funkcja, która faktycznie zarządza zrzucaniem zawartości bazy do pliku.
        Domyślnie nadpisywane są wszystkie pliki i foldery.
        
        Parametr `locations` mówi, czy dampowany ma zostać także plik z lokacja-
        mi. Podobnie `markers` odpowiada za dumpowanie markerów.
        
        Podając country_code (np, US, PL etc.) dumpujemy tylko dane z lokaliza-
        cji zawartych w konkretnym kraju.
        """
        if country_code:
            queryset = Country.objects.filter(code=country_code)
        else:
            queryset = Country.objects.all()

        for country in queryset:
            if dump_markers:
                markers = self.get_markers(country)
                serializer = MapPointerSerializer(markers, many=True)
                self.save_file_(serializer.data, country.pk)
            if dump_locations:
                locations = Location.objects.filter(country_code=country.code)
                serializer = MapLocationSerializer(locations, many=True)
                self.save_locations_(serializer.data, country.pk)

    def import_data(self, country_pk=None):
        """
        Funkcja umożliwiająca import znaczników z plików do postaci rozpoznawalnej
        przez serializery. Umożliwia to wyświetlenie danych na mapie.
        """
        markers = []
        
        if country_pk:
            locations = self.load_locations_(country_pk)
            pointers  = self.load_file_(country_pk)
            markers = pointers + locations

        for country in Country.objects.all():
            #markers += self.load_locations_(country.pk)
            #markers += self.load_file_(country.pk)
            pass

        return markers


# Sygnały obsługujące tworzenie/usuwanie markerów dla różnych obiektów.
# ---------------------------------------------------------------------

def dump_location_markers(sender, instance, created, **kwargs):
    """
    Funkcja zapisująca markery dla lokalizacji w kraju, do którego należy nowo
    utworzona/wyedytowana lokalizacja (sender). Funkcja nie sprawdza, czy sender
    faktycznie jest instancją modelu Location.
    """
    if not instance.latitude or not instance.longitude: return False
    cjs = CountryJSONStorage()
    cjs.dump_data(instance.country_code, True, False)


def dump_object_markers(sender, instance, created, **kwargs):
    """
    Funkcja zrzuca do pliku wszystkie informacje o markerach w kraju odpowiada-
    jącym nowo utworzonemu/wyedytowanemu markerowi. Należy przekazać instancję
    obiektu MapPointer.
    """
    cjs = CountryJSONStorage()
    cjs.dump_data(instance.content_object.location.country_code, False, True)
