# Generated by Django 3.1.2 on 2021-03-10 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0026_dataprovider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='buyer_id',
            field=models.CharField(max_length=50, verbose_name='Buyer ID'),
        ),
    ]
