# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerdemand',
            name='lang',
            field=models.CharField(default=b'pl', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lang',
            field=models.CharField(default=b'pl', max_length=7, choices=[(b'en', b'English'), (b'pl', b'Polski'), (b'es', b'Espa\xc3\xb1ol (soon)'), (b'de', b'Deutsch'), (b'pt', b'Portugu\xc3\xaas (soon)'), (b'fr', b'Fran\xc3\xa7ais (soon)'), (b'it', b'Italiano (soon)'), (b'cz', b'Ce\xc5\xa1tina (soon)')]),
            preserve_default=True,
        ),
    ]
