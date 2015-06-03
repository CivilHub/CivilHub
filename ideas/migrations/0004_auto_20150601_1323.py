# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0003_idea_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='status',
            field=models.PositiveIntegerField(default=1, choices=[(1, 'active'), (2, 'in progress'), (3, 'completed'), (4, 'project')]),
            preserve_default=True,
        ),
    ]
