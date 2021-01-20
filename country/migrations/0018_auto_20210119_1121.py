# Generated by Django 3.1.2 on 2021-01-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0017_auto_20210119_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='buyer_name',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='Buyer name'),
        ),
        migrations.AlterField(
            model_name='goodsservicescategory',
            name='category_name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='supplier_name',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='Supplier name'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='contract_date',
            field=models.DateField(db_index=True, null=True, verbose_name='Contract date'),
        ),
    ]
