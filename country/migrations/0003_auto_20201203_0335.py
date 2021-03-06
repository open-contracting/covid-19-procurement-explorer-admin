# Generated by Django 3.1.2 on 2020-12-03 03:35

from django.db import migrations, models


def migrate_data_forward(apps, schema_editor):
    Country = apps.get_model("country", "Country")

    for instance in Country.objects.all():
        print(f"Generating slug for {instance}")
        instance.save()  # Will trigger slug update


def migrate_data_backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("country", "0002_country_country_code_alpha_2"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="slug",
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="country",
            name="name",
            field=models.CharField(max_length=50, unique=True, verbose_name="Name"),
        ),
        migrations.RunPython(
            migrate_data_forward,
            migrate_data_backward,
        ),
    ]
