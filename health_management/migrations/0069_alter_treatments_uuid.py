# Generated by Django 4.2.2 on 2023-06-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0068_feepayement_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatments',
            name='uuid',
            field=models.CharField(blank=True, db_index=True, max_length=150, null=True),
        ),
    ]
