# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0005_businessapplication_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessapplication',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
