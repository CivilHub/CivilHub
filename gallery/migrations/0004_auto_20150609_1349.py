# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_contentobjectgallery_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentobjectpicture',
            options={'ordering': ['-date_uploaded'], 'verbose_name': 'picture', 'verbose_name_plural': 'pictures'},
        ),
        migrations.AlterField(
            model_name='contentobjectgallery',
            name='name',
            field=models.CharField(default='', max_length=64, verbose_name='name', blank=True),
            preserve_default=True,
        ),
    ]
