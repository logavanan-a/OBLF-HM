# Generated by Django 4.1.7 on 2023-05-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0050_clinicprofile_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicprofile',
            name='code',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
