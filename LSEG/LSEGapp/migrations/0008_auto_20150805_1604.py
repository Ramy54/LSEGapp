# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0007_auto_20150804_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentvariablestemplate',
            name='variable',
            field=models.ForeignKey(to='LSEGapp.Variable', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
