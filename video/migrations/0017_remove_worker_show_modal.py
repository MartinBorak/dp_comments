# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 23:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0016_worker_show_modal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='show_modal',
        ),
    ]
