# Generated by Django 4.2.2 on 2023-06-23 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0077_alter_health_uuid_alter_treatments_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feepayement',
            name='uuid',
            field=models.CharField(blank=True, db_index=True, max_length=150, null=True, unique=True),
        ),
    ]