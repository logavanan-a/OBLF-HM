# Generated by Django 4.2.2 on 2023-06-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0079_alter_treatments_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='uuid',
            field=models.CharField(blank=True, db_index=True, max_length=150, null=True, unique=True),
        ),
    ]
