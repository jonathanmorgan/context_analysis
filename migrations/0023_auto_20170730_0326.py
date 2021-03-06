# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 03:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_text', '0018_auto_20160924_1704'),
        ('context_analysis', '0022_auto_20170728_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reliability_names_evaluation',
            name='merged_from_article_data',
        ),
        migrations.RemoveField(
            model_name='reliability_names_evaluation',
            name='merged_to_article_data',
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='merged_from_article_datas',
            field=models.ManyToManyField(related_name='rne_merged_from_article_data', to='context_text.Article_Data'),
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='merged_to_article_datas',
            field=models.ManyToManyField(related_name='rne_merged_to_article_data', to='context_text.Article_Data'),
        ),
    ]
