# Generated by Django 3.2.6 on 2023-02-22 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application_masters', '0016_alter_village_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicines',
            name='medicine_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='MedicinesReportCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Inactive'), (2, 'Active')], db_index=True, default=2)),
                ('server_created_on', models.DateTimeField(auto_now_add=True)),
                ('server_modified_on', models.DateTimeField(auto_now=True)),
                ('sync_status', models.PositiveIntegerField(default=2)),
                ('name', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='createdapplication_masters_medicinesreportcategory_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modifiedapplication_masters_medicinesreportcategory_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
