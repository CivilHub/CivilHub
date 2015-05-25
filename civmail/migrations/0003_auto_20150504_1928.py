# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('civmail', '0002_massemail_scheduled_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='massemail',
            name='body_cz',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_de',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_en',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_es',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_fr',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_it',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_pl',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='body_pt',
            field=models.TextField(default='', null=True, verbose_name='message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_cz',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_de',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_en',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_es',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_fr',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_it',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_pl',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massemail',
            name='subject_pt',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='subject'),
            preserve_default=True,
        ),
    ]
