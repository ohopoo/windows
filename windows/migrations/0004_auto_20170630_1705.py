# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-30 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows', '0003_auto_20170630_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]