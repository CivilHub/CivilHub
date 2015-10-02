# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20150504_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simplepoll',
            name='name_cz',
        ),
        migrations.RemoveField(
            model_name='simplepoll',
            name='name_it',
        ),
        migrations.RemoveField(
            model_name='simplepollanswer',
            name='text_cz',
        ),
        migrations.RemoveField(
            model_name='simplepollanswer',
            name='text_it',
        ),
        migrations.RemoveField(
            model_name='simplepollquestion',
            name='text_cz',
        ),
        migrations.RemoveField(
            model_name='simplepollquestion',
            name='text_it',
        ),
    ]
