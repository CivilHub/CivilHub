# -*- coding: utf-8 -*-
"""
Moduł zarządzający zrzutem danych z bazy do plików JSON. Pliki są posegregowane
na foldery państw odpowiadające modelom `country` w bazie.
"""
import os, json
from django.conf import settings
from maps.serializers import MapPointerSerializer
from maps.models import MapPointer
from .models import Country


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

    def load_file_(self, country_pk):
        """
        Metoda odczytująca plik JSON i zwracająca zserializowaną listę obiektów
        w formacie JSON.
        """
        f = open(os.path.join(self.path, str(country_pk), 'markers.json'))
        return json.loads(f.read())

    def get_queryset(self, country_pk=None):
        """
        Funkcja, która wykonuje faktyczne zapytanie do bazy. Parametr `country`
        jest opcjonalny i oznacza ID kraju, który nas interesuje. Jeżeli nie
        zostanie podany, wybrane będą wszystkie kraje.
        """
        if country_pk:
            map_pointers = []
            country = Country.objects.get(pk=country_pk)
            for map_pointer in MapPointer.objects.all():
                if map_pointer.content_object.location == country.location:
                    map_pointers.append(map_pointer)
                if map_pointer.content_object.location in country.location.get_ancestor_chain(response='QUERYSET'):
                    map_pointers.append(map_pointer)
            return map_pointers
        else:
            return MapPointer.objects.all()

    def get_markers(self, country_pk):
        """
        Funkcja "zbiera" wszystkie markery dla danego kraju (country_pk).
        """
        map_pointers = []
        country = Country.objects.get(pk=country_pk)
        for map_pointer in MapPointer.objects.all():
            if map_pointer.content_object.location == country.location:
                map_pointers.append(map_pointer)
            if map_pointer.content_object.location in country.location.get_ancestor_chain(response='QUERYSET'):
                map_pointers.append(map_pointer)
        return map_pointers

    def dump_data(self):
        """
        Funkcja, która faktycznie zarządza zrzucaniem zawartości bazy do pliku.
        Domyślnie nadpisywane są wszystkie pliki i foldery.
        """
        for country in Country.objects.all():
            markers = self.get_markers(country.pk)
            serializer = MapPointerSerializer(markers, many=True)
            print serializer.data
            self.save_file_(serializer.data, country.pk)

    def import_data(self, country_pk=None):
        """
        Funkcja umożliwiająca import znaczników z plików do postaci rozpoznawalnej
        przez serializery. Umożliwia to wyświetlenie danych na mapie.
        """
        if country_pk:
            return self.load_file_(country_pk)
            
        markers = []
        for country in Country.objects.all():
            markers.append(self.load_file_(country.pk))
        return markers