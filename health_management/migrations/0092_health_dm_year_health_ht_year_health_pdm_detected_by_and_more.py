# Generated by Django 4.2.2 on 2023-12-05 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('health_management', '0091_prescriptionprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='health',
            name='dm_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='health',
            name='ht_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='health',
            name='pdm_detected_by',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='health',
            name='pdm_source_treatment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='health',
            name='pdm_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='health',
            name='pht_detected_by',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='health',
            name='pht_source_treatment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='health',
            name='pht_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PatientComorbids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(1, 'Inactive'), (2, 'Active')], db_index=True, default=2)),
                ('server_created_on', models.DateTimeField(auto_now_add=True)),
                ('server_modified_on', models.DateTimeField(auto_now=True)),
                ('sync_status', models.PositiveIntegerField(default=2)),
                ('uuid', models.CharField(blank=True, db_index=True, max_length=150, null=True, unique=True)),
                ('patient_uuid', models.CharField(blank=True, db_index=True, max_length=150, null=True)),
                ('month_year', models.DateField(blank=True, null=True)),
                ('co_morbid_id', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]