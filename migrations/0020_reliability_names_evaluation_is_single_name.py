# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_analysis', '0019_reliability_names_evaluation_is_automated_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='is_single_name',
            field=models.BooleanField(default=False),
        ),
    ]
