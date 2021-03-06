# Generated by Django 3.1.7 on 2021-03-31 15:26

import content.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0044_auto_20210316_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countrypartner',
            options={'verbose_name': 'Country Partner', 'verbose_name_plural': 'Country Partners'},
        ),
        migrations.AlterModelOptions(
            name='dataimport',
            options={'verbose_name': 'Data Import', 'verbose_name_plural': 'Data Imports'},
        ),
        migrations.AlterModelOptions(
            name='eventspage',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='insightspage',
            options={'verbose_name': 'News & Blog', 'verbose_name_plural': 'News & Blogs'},
        ),
        migrations.AlterModelOptions(
            name='resourcespage',
            options={'verbose_name': 'Resource', 'verbose_name_plural': 'Resources'},
        ),
        migrations.AlterModelOptions(
            name='staticpage',
            options={'verbose_name': 'Static Page', 'verbose_name_plural': 'Static Pages'},
        ),
        migrations.AddField(
            model_name='dataimport',
            name='validated',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='dataimport',
            name='import_file',
            field=models.FileField(null=True, upload_to='documents', validators=[content.validators.validate_file_extension]),
        ),
    ]
