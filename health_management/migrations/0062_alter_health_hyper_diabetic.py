# Generated by Django 4.2.2 on 2023-06-22 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0061_alter_health_dm_years_alter_health_ht_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='health',
            name='hyper_diabetic',
            field=models.IntegerField(default=0),
        ),
    ]