# Generated by Django 3.1.2 on 2021-03-10 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0028_auto_20210310_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsservices',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goods_services', to='country.buyer'),
        ),
        migrations.AddField(
            model_name='goodsservices',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goods_services', to='country.supplier'),
        ),
    ]
