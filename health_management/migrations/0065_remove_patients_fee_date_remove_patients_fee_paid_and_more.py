# Generated by Django 4.2.2 on 2023-06-22 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0064_remove_patients_age_remove_patients_last_visit_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patients',
            name='fee_date',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='fee_paid',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='fee_status',
        ),
    ]