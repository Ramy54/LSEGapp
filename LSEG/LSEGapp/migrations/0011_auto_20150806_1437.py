# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0010_auto_20150806_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentvariables',
            name='variable',
            field=models.ForeignKey(to='LSEGapp.Variable'),
        ),
        migrations.AlterField(
            model_name='componentvariablestemplate',
            name='component',
            field=models.ForeignKey(to='LSEGapp.Component'),
        ),
    ]
