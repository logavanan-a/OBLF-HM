# Generated by Django 3.2.6 on 2022-12-15 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0013_auto_20221213_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='dosage',
        ),
    ]