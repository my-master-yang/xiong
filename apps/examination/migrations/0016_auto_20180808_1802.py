# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-08 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0015_auto_20180808_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercard',
            name='start_time',
            field=models.IntegerField(default=0, verbose_name='开始时间'),
        ),
    ]
