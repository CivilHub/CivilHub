# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_remove_idea_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='status',
            field=models.PositiveIntegerField(default=1, choices=[(1, 'active'), (2, 'completed'), (3, 'in progress'), (4, 'project')]),
            preserve_default=True,
        ),
    ]
