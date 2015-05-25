# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_simplepollanswerset_timestamp'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='simplepollanswerset',
            unique_together=set([('user', 'poll', 'question')]),
        ),
    ]
