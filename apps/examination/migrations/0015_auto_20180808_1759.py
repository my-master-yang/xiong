# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-08 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0014_auto_20180808_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercard',
            name='start_time',
            field=models.IntegerField(default=0, max_length=20, verbose_name='开始时间'),
        ),
        migrations.AlterField(
            model_name='question',
            name='add_time',
            field=models.DateTimeField(default=None, verbose_name='添加时间'),
        ),
    ]
