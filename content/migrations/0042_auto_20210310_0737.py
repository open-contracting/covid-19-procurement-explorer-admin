# Generated by Django 3.1.2 on 2021-03-10 07:37

import content.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0041_auto_20210309_1050"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventspage",
            name="organisation",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
