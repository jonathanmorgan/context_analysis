# Generated by Django 3.1.2 on 2020-12-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_text', '0033_auto_20201218_1723'),
        ('context_analysis', '0035_auto_20201018_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reliability_names_eval',
            name='merged_from_ad',
            field=models.ManyToManyField(blank=True, related_name='rne_merged_from_ad', to='context_text.Article_Data'),
        ),
        migrations.AlterField(
            model_name='reliability_names_eval',
            name='merged_to_ad',
            field=models.ManyToManyField(blank=True, related_name='rne_merged_to_ad', to='context_text.Article_Data'),
        ),
    ]
