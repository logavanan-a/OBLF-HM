# Generated by Django 3.2.6 on 2023-01-17 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0029_auto_20230117_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patients',
            options={'ordering': ['village'], 'verbose_name_plural': 'Patients'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_no',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
