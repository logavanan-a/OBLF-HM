# Generated by Django 4.1.7 on 2023-04-03 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0041_villageprofile_age_villageprofile_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='villageprofile',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='village_profile_image/%y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='villageprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
