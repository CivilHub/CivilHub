# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_socialproject_idea'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='tasks',
            field=models.ManyToManyField(related_name='attachments', null=True, verbose_name='tasks', to='projects.Task', blank=True),
            preserve_default=True,
        ),
    ]
