# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0015_auto_20161106_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='show_modal',
            field=models.BooleanField(default=True),
        ),
    ]
