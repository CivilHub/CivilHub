# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_cz',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_de',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_es',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_fr',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_it',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_pl',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='description_pt',
            field=models.TextField(default='', max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_cz',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_de',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_es',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_fr',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_it',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_pl',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='name_pt',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
    ]
