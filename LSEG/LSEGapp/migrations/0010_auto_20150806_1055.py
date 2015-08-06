# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0009_auto_20150805_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostbusinessapplication',
            name='business_application',
        ),
        migrations.RemoveField(
            model_name='hostbusinessapplication',
            name='host',
        ),
        migrations.AlterField(
            model_name='rolecomponents',
            name='component',
            field=models.ForeignKey(to='LSEGapp.Component'),
        ),
        migrations.DeleteModel(
            name='HostBusinessApplication',
        ),
    ]
