# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0011_auto_20150806_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentvariables',
            name='role_component',
            field=models.ForeignKey(to='LSEGapp.RoleComponents'),
        ),
        migrations.AlterField(
            model_name='hostrole',
            name='host',
            field=models.ForeignKey(to='LSEGapp.Host'),
        ),
        migrations.AlterField(
            model_name='rolebusinessapplication',
            name='role',
            field=models.ForeignKey(to='LSEGapp.Role'),
        ),
        migrations.AlterField(
            model_name='rolecomponents',
            name='host_role',
            field=models.ForeignKey(to='LSEGapp.HostRole'),
        ),
        migrations.AlterField(
            model_name='rolecomponentstemplate',
            name='role',
            field=models.ForeignKey(to='LSEGapp.Role'),
        ),
        migrations.AlterField(
            model_name='variable',
            name='default_value',
            field=models.CharField(max_length=200),
        ),
    ]
