# Generated by Django 3.1.7 on 2021-04-01 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0030_auto_20210331_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='covid19_preparedness',
        ),
        migrations.RemoveField(
            model_name='country',
            name='covid19_procurement_policy',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_age_dist_0_14',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_age_dist_15_24',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_age_dist_25_54',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_age_dist_55_64',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_age_dist_65_above',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_gender_dist_female',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_gender_dist_male',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_income_avg',
        ),
        migrations.RemoveField(
            model_name='country',
            name='equity_unemployment_rate',
        ),
        migrations.RemoveField(
            model_name='country',
            name='procurement_annual_public_spending',
        ),
        migrations.RemoveField(
            model_name='country',
            name='procurement_covid_spending',
        ),
        migrations.RemoveField(
            model_name='country',
            name='procurement_gdp_pc',
        ),
        migrations.RemoveField(
            model_name='country',
            name='procurement_total_market_pc',
        ),
    ]