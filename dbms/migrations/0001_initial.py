# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-18 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=40)),
                ('emails', models.CharField(max_length=100)),
            ],
        ),
    ]
