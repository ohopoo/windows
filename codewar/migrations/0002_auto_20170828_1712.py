# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-28 10:12
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('codewar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]