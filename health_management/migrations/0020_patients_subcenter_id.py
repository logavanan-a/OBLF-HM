# Generated by Django 3.2.6 on 2022-12-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0019_alter_patients_village'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='subcenter_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
