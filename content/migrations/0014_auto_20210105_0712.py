# Generated by Django 3.1.2 on 2021-01-05 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0013_countrypartner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="countrypartner",
            name="logo",
            field=models.ImageField(upload_to="country/partner/logo"),
        ),
    ]
