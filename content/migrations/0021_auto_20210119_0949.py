# Generated by Django 3.1.2 on 2021-01-19 09:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_auto_20210119_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventspage',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='insightspage',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='resourcespage',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]