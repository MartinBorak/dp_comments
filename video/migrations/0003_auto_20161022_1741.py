# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-22 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20161018_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='neutral',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='reactions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='neutral',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reply',
            name='reactions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
