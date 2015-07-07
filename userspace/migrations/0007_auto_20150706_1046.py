# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0006_auto_20150616_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='description_cz',
        ),
        migrations.RemoveField(
            model_name='badge',
            name='description_it',
        ),
        migrations.RemoveField(
            model_name='badge',
            name='name_cz',
        ),
        migrations.RemoveField(
            model_name='badge',
            name='name_it',
        ),
        migrations.AddField(
            model_name='closeaccountdemand',
            name='is_deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lang',
            field=models.CharField(default=b'pl', max_length=7, verbose_name='language', choices=[(b'en', b'English'), (b'pl', b'Polski'), (b'es', b'Espa\xc3\xb1ol'), (b'de', b'Deutsch'), (b'pt', b'Portugu\xc3\xaas'), (b'fr', b'Fran\xc3\xa7ais')]),
            preserve_default=True,
        ),
    ]
