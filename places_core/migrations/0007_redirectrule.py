# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places_core', '0006_auto_20150609_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_in', models.URLField()),
                ('url_out', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
