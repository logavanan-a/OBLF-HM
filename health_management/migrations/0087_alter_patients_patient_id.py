# Generated by Django 4.2.2 on 2023-08-04 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0086_alter_patients_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='patient_id',
            field=models.CharField(blank=True, db_index=True, max_length=150, null=True, unique=True),
        ),
    ]
