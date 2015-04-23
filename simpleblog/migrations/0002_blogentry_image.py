# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import places_core.models


class Migration(migrations.Migration):

    dependencies = [
        ('simpleblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogentry',
            name='image',
            field=models.ImageField(default=b'img/item.png', upload_to=places_core.models.get_image_upload_path, verbose_name='image', blank=True),
            preserve_default=True,
        ),
    ]
