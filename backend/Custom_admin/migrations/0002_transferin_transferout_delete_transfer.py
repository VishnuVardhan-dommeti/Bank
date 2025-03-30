# Generated by Django 4.2.11 on 2025-03-29 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Custom_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_transfers', to='Custom_admin.account')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_in', to='Custom_admin.account')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_in', to='Custom_admin.transaction')),
            ],
            options={
                'verbose_name_plural': 'Transfers In',
            },
        ),
        migrations.CreateModel(
            name='TransferOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_out', to='Custom_admin.account')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transfers', to='Custom_admin.account')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_out', to='Custom_admin.transaction')),
            ],
            options={
                'verbose_name_plural': 'Transfers Out',
            },
        ),
        migrations.DeleteModel(
            name='Transfer',
        ),
    ]
