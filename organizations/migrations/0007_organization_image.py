# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import organizations.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_auto_20150420_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='image',
            field=models.ImageField(default='img/organizations/default.jpg', upload_to=organizations.models.background_upload_path, verbose_name='background image'),
            preserve_default=True,
        ),
    ]
