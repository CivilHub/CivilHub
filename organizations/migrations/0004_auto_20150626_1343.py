# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20150508_1138'),
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
            model_name='invitation',
            name='email',
            field=models.EmailField(default='', max_length=75, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('email', 'organization')]),
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='user',
        ),
    ]
