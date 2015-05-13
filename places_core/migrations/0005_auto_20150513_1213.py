# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places_core', '0004_auto_20150416_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTermRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=255, verbose_name='search term')),
                ('ip_address', models.IPAddressField(null=True, verbose_name='ip address', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('content_types', models.CharField(default='', max_length=255, verbose_name='content types', blank=True)),
                ('user', models.ForeignKey(verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'search record',
                'verbose_name_plural': 'search records',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='reason',
            field=models.PositiveIntegerField(default=12, choices=[(1, 'Pornography'), (2, 'Violence/indicent content'), (3, 'Insults/spread of hatred'), (4, 'Dangerious activities'), (5, 'Usage of children'), (6, 'Spam or other misleading content'), (7, 'Violence of my copyrights'), (8, 'Violence of my privacy'), (9, 'Other legal claims'), (10, 'Duplicate'), (11, 'False information'), (12, 'Is not suitable')]),
            preserve_default=True,
        ),
    ]
