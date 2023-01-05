# Generated by Django 3.2.6 on 2023-01-05 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application_masters', '0015_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('health_management', '0023_alter_homevisit_home_vist'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Inactive'), (2, 'Active')], db_index=True, default=2)),
                ('server_created_on', models.DateTimeField(auto_now_add=True)),
                ('server_modified_on', models.DateTimeField(auto_now=True)),
                ('sync_status', models.PositiveIntegerField(default=2)),
                ('date_of_creation', models.DateTimeField(blank=True, null=True)),
                ('unit_price', models.PositiveIntegerField(blank=True, null=True)),
                ('no_of_units', models.PositiveIntegerField(blank=True, null=True)),
                ('opening_stock', models.IntegerField(blank=True, null=True)),
                ('closing_stock', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='createdhealth_management_medicinestock_related', to=settings.AUTH_USER_MODEL)),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application_masters.medicines')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modifiedhealth_management_medicinestock_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DrugDispensation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Inactive'), (2, 'Active')], db_index=True, default=2)),
                ('server_created_on', models.DateTimeField(auto_now_add=True)),
                ('server_modified_on', models.DateTimeField(auto_now=True)),
                ('sync_status', models.PositiveIntegerField(default=2)),
                ('units_dispensed', models.PositiveIntegerField(blank=True, null=True)),
                ('date_of_dispensation', models.DateTimeField(blank=True, null=True)),
                ('opening_stock', models.IntegerField(blank=True, null=True)),
                ('closing_stock', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='createdhealth_management_drugdispensation_related', to=settings.AUTH_USER_MODEL)),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application_masters.medicines')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modifiedhealth_management_drugdispensation_related', to=settings.AUTH_USER_MODEL)),
                ('village', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='application_masters.village')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
