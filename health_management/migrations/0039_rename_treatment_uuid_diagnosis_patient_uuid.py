# Generated by Django 4.1.7 on 2023-03-15 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0038_alter_diagnosis_created_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diagnosis',
            old_name='treatment_uuid',
            new_name='patient_uuid',
        ),
    ]
