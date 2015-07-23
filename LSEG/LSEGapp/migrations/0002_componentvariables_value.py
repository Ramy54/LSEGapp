# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentvariables',
            name='value',
            field=models.CharField(max_length=50, default=''),
        ),
    ]
