# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0003_idea_status'),
        ('projects', '0007_attachment_mime_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialproject',
            name='idea',
            field=models.ForeignKey(related_name='projects', verbose_name='idea', blank=True, to='ideas.Idea', null=True),
            preserve_default=True,
        ),
    ]
