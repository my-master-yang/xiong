# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-11 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0004_auto_20180607_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampaper',
            name='examLessonNum',
            field=models.IntegerField(default=1, verbose_name='试卷编号'),
        ),
    ]
