# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-08 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0029_auto_20180808_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answercard',
            name='number_id',
        ),
        migrations.RemoveField(
            model_name='answercard',
            name='start_time',
        ),
    ]
