# Generated by Django 3.2.6 on 2022-12-13 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application_masters', '0008_medicines'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicines',
            old_name='types',
            new_name='type',
        ),
    ]
