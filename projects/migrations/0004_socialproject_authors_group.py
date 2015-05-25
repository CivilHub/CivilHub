# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etherpad', '0001_initial'),
        ('projects', '0003_socialforumentry_is_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialproject',
            name='authors_group',
            field=models.ForeignKey(blank=True, to='etherpad.EtherpadGroup', null=True),
            preserve_default=True,
        ),
    ]
