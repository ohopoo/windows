# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-29 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows', '0005_auto_20170722_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='vote_team',
            field=models.BooleanField(default=False),
        ),
    ]
