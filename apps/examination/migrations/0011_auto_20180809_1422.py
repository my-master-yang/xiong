# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-09 06:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0010_auto_20180809_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercard',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 8, 9, 14, 22, 33, 360410), null=True, verbose_name='开始时间'),
        ),
    ]
