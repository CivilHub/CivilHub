# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapvotes', '0002_marker_voting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='marker',
            field=models.ForeignKey(related_name='votes', verbose_name='marker', to='mapvotes.Marker'),
            preserve_default=True,
        ),
    ]
