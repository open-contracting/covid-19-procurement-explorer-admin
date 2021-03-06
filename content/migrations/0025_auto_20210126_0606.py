# Generated by Django 3.1.2 on 2021-01-26 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("country", "0018_auto_20210119_1121"),
        ("content", "0024_auto_20210126_0606"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataimport",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="country.country",
            ),
        ),
    ]
