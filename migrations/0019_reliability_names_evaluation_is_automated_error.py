# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sourcenet_analysis', '0018_auto_20170709_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='is_automated_error',
            field=models.BooleanField(default=False),
        ),
    ]