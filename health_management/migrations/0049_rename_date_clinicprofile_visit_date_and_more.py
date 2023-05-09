# Generated by Django 4.1.7 on 2023-05-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0048_alter_patients_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clinicprofile',
            old_name='date',
            new_name='visit_date',
        ),
        migrations.AddField(
            model_name='clinicprofile',
            name='family_history',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]