# Generated by Django 3.1.7 on 2021-05-03 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0049_auto_20210503_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insightspage',
            name='featured',
            field=models.CharField(choices=[('true', 'Yes'), ('false', 'No')], default=False, max_length=15, verbose_name='Featured ?'),
        ),
    ]
