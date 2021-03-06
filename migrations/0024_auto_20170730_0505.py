# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_analysis', '0023_auto_20170730_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reliability_names_evaluation',
            name='article_datas',
            field=models.ManyToManyField(blank=True, related_name='rne_article_data', to='context_text.Article_Data'),
        ),
        migrations.AlterField(
            model_name='reliability_names_evaluation',
            name='merged_from_article_datas',
            field=models.ManyToManyField(blank=True, related_name='rne_merged_from_article_data', to='context_text.Article_Data'),
        ),
        migrations.AlterField(
            model_name='reliability_names_evaluation',
            name='merged_to_article_datas',
            field=models.ManyToManyField(blank=True, related_name='rne_merged_to_article_data', to='context_text.Article_Data'),
        ),
    ]
