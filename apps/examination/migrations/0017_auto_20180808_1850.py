# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-08 10:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0016_auto_20180808_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercard',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='开始时间'),
        ),
    ]
