# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0014_auto_20161104_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='reply',
            name='reply_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
