# Generated by Django 4.2.2 on 2023-06-22 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0075_rename_payment_date_feepayement_fee_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feepayement',
            old_name='fee_date',
            new_name='payment_date',
        ),
    ]
