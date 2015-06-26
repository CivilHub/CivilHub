# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.youtube_field


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0007_remove_vote_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description_cz',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_it',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_cz',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_it',
        ),
        migrations.AddField(
            model_name='idea',
            name='video_url',
            field=utils.youtube_field.YoutubeUrlField(null=True, verbose_name='Youtube video', blank=True),
            preserve_default=True,
        ),
    ]
