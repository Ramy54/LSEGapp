# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LSEGapp', '0003_variable_editable'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleBusinessApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('business_application', models.ForeignKey(to='LSEGapp.BusinessApplication')),
                ('role', models.ForeignKey(to='LSEGapp.Role')),
            ],
            options={
                'verbose_name': '04- Role Business Application',
                'verbose_name_plural': '04 - Role Business Applications',
            },
        ),
    ]
