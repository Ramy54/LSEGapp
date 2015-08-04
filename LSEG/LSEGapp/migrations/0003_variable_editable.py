# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0002_componentvariables_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='editable',
            field=models.BooleanField(default=True),
        ),
    ]
