# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0004_rolebusinessapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessapplication',
            name='prefix',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
