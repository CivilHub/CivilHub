# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_licenses(apps, schema_editor):
    ImageLicense = apps.get_model("locations", "ImageLicense")
    names = [
        u'All Rights Reserved',
        u'CC_BY (Creative Commons)',
        u'CC_NC (Creative Commons)',
        u'CC_SA (Creative Commons)',
        u'CC_ND (Creative Commons)', ]
    labels = [
        u'Bez pisemnej (mail, umowa na papierze) zgody autora korzystać nie możemy.',
        u'Najszersza, możemy używać bez ograniczeń.',
        u'Można rozprowadzać, kopiować do celów niekomercyjnych.',
        u'Wolno rozprowadzać, kopiować na licencji identycznej jak autora; jeśli zmieniamy zdjęcie musimy je udostępniać na tej samej licencji.',
        u'Kopiowanie, rozprowadzania tylko w oryginalnej całości.', ]
    for i in range(len(names)):
        fields = {}
        name_fields = [x.name for x in ImageLicense._meta.fields if 'name' in x.name]
        desc_fields = [x.name for x in ImageLicense._meta.fields if 'description' in x.name]
        for f in name_fields:
            fields[f] = names[i]
        for f in desc_fields:
            fields[f] = labels[i]
        il = ImageLicense.objects.create(**fields)


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_auto_20150707_1310'),
    ]

    operations = [
        migrations.RunPython(create_licenses)
    ]
