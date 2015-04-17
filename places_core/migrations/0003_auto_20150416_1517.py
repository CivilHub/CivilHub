# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places_core', '0002_abusereport_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abusereport',
            name='reason',
            field=models.PositiveIntegerField(default=12, choices=[(1, 'Tre\u015b\u0107\xa0pornograficzna'), (2, 'Przemoc/tre\u015bci budz\u0105ce odraz\u0119'), (3, 'Obra\u017canie/szerzenie nienawi\u015bci'), (4, 'Dzia\u0142ania niebezpieczne'), (5, 'Wykorzystywanie dzieci'), (6, 'Spam lub tre\u015bci wprowadzaj\u0105ce w b\u0142\u0105d'), (7, 'Naruszenie moich praw autorskich'), (8, 'Naruszenie moich praw prywatno\u015bci'), (9, 'Inne roszczenia prawne'), (10, 'Duplikat'), (11, 'Informacja nieprawdziwa'), (12, 'Nie nadaje si\u0119')]),
            preserve_default=True,
        ),
    ]
