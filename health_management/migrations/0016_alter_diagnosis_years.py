# Generated by Django 3.2.6 on 2022-12-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0015_prescription_dosage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='years',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]