# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-07 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0002_auto_20180606_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exampaper',
            name='examFile',
            field=models.FilePathField(default='/file/', match='*.xls', verbose_name='考试试卷文件'),
        ),
    ]
