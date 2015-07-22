# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': '02- Business Applications',
                'verbose_name': '02- Business Application',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': '06- Components',
                'verbose_name': '06- Component',
            },
        ),
        migrations.CreateModel(
            name='ComponentVariables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '12- Components Variables',
                'verbose_name': '12- Component Variables',
            },
        ),
        migrations.CreateModel(
            name='ComponentVariablesTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.ForeignKey(to='LSEGapp.Component')),
            ],
            options={
                'verbose_name_plural': '10- Component Variables Templates',
                'verbose_name': '10- Component Variables Template',
            },
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': '01- Environments',
                'verbose_name': '01- Environment',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('environment', models.ForeignKey(to='LSEGapp.Environment')),
            ],
            options={
                'verbose_name_plural': '03- Hosts',
                'verbose_name': '03- Host',
            },
        ),
        migrations.CreateModel(
            name='HostBusinessApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_application', models.ForeignKey(to='LSEGapp.BusinessApplication')),
                ('host', models.ForeignKey(to='LSEGapp.Host')),
            ],
            options={
                'verbose_name_plural': '04 - Host Business Applications',
                'verbose_name': '04- Host Business Application',
            },
        ),
        migrations.CreateModel(
            name='HostRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(to='LSEGapp.Host')),
            ],
            options={
                'verbose_name_plural': '08- Host Roles',
                'verbose_name': '08- Host Role',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': '05- Roles',
                'verbose_name': '05- Role',
            },
        ),
        migrations.CreateModel(
            name='RoleComponents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.ForeignKey(to='LSEGapp.Component')),
                ('host_role', models.ForeignKey(to='LSEGapp.HostRole')),
            ],
            options={
                'verbose_name_plural': '11- Roles Components',
                'verbose_name': '11- Role Components',
            },
        ),
        migrations.CreateModel(
            name='RoleComponentsTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.ForeignKey(to='LSEGapp.Component')),
                ('role', models.ForeignKey(to='LSEGapp.Role')),
            ],
            options={
                'verbose_name_plural': '09- Role Components Templates',
                'verbose_name': '09- Role Components Template',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('default_value', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('required', models.BooleanField()),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': '07- Variables',
                'verbose_name': '07- Variable',
            },
        ),
        migrations.AddField(
            model_name='hostrole',
            name='role',
            field=models.ForeignKey(to='LSEGapp.Role'),
        ),
        migrations.AddField(
            model_name='componentvariablestemplate',
            name='variable',
            field=models.ForeignKey(to='LSEGapp.Variable'),
        ),
        migrations.AddField(
            model_name='componentvariables',
            name='role_component',
            field=models.ForeignKey(to='LSEGapp.RoleComponents'),
        ),
        migrations.AddField(
            model_name='componentvariables',
            name='variable',
            field=models.ForeignKey(to='LSEGapp.Variable'),
        ),
    ]
