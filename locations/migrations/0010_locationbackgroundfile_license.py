# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0009_remove_locationbackgroundfile_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationbackgroundfile',
            name='license',
            field=models.ForeignKey(verbose_name='license', blank=True, to='locations.ImageLicense', null=True),
            preserve_default=True,
        ),
    ]
