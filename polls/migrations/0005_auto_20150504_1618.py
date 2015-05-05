# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20150504_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplepoll',
            name='name_cz',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_de',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_es',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_fr',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_it',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_pl',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepoll',
            name='name_pt',
            field=models.CharField(max_length=200, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_cz',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_de',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_en',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_es',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_fr',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_it',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_pl',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='text_pt',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='answer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_cz',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_de',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_en',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_es',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_fr',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_it',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_pl',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollquestion',
            name='text_pt',
            field=models.TextField(default='', null=True, verbose_name='question'),
            preserve_default=True,
        ),
    ]
