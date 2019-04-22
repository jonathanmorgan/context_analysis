# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-03 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('context_text', '0018_auto_20160924_1704'),
        ('context_analysis', '0015_reliability_names_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='is_ground_truth_fixed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='merged_from_article_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rne_merged_from_article_data', to='context_text.Article_Data'),
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='merged_from_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='merged_to_article_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rne_merged_to_article_data', to='context_text.Article_Data'),
        ),
        migrations.AddField(
            model_name='reliability_names_evaluation',
            name='merged_to_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reliability_names_evaluation',
            name='article_datas',
            field=models.ManyToManyField(related_name='rne_article_data', to='context_text.Article_Data'),
        ),
    ]
