# Generated by Django 3.2.6 on 2022-12-19 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0016_alter_diagnosis_years'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='seq_no',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
