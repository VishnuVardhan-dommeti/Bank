# Generated by Django 4.2.11 on 2025-03-29 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Custom_admin', '0003_account_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='opening_date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='overdraft_limit',
        ),
        migrations.RemoveField(
            model_name='account',
            name='status',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='national_id',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='risk_category',
        ),
    ]
