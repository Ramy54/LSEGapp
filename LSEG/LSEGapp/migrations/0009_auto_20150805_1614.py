# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0008_auto_20150805_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentvariables',
            name='role_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.RoleComponents'),
        ),
        migrations.AlterField(
            model_name='componentvariables',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Variable'),
        ),
        migrations.AlterField(
            model_name='componentvariablestemplate',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Component'),
        ),
        migrations.AlterField(
            model_name='host',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Environment'),
        ),
        migrations.AlterField(
            model_name='hostbusinessapplication',
            name='business_application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.BusinessApplication'),
        ),
        migrations.AlterField(
            model_name='hostbusinessapplication',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Host'),
        ),
        migrations.AlterField(
            model_name='hostrole',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Host'),
        ),
        migrations.AlterField(
            model_name='hostrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Role'),
        ),
        migrations.AlterField(
            model_name='rolebusinessapplication',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Role'),
        ),
        migrations.AlterField(
            model_name='rolecomponents',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Component'),
        ),
        migrations.AlterField(
            model_name='rolecomponents',
            name='host_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.HostRole'),
        ),
        migrations.AlterField(
            model_name='rolecomponentstemplate',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Component'),
        ),
        migrations.AlterField(
            model_name='rolecomponentstemplate',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LSEGapp.Role'),
        ),
    ]
