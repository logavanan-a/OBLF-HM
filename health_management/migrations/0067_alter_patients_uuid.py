# Generated by Django 4.2.2 on 2023-06-22 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0066_feepayement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='uuid',
            field=models.CharField(blank=True, db_index=True, max_length=150, null=True),
        ),
    ]
