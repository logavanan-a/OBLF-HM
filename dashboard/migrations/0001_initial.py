# Generated by Django 3.2.6 on 2023-02-06 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardWidgetSummaryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Inactive'), (2, 'Active')], db_index=True, default=2)),
                ('server_created_on', models.DateTimeField(auto_now_add=True)),
                ('server_modified_on', models.DateTimeField(auto_now=True)),
                ('sync_status', models.PositiveIntegerField(default=2)),
                ('log_key', models.CharField(max_length=500, unique=True)),
                ('last_successful_update', models.DateTimeField(blank=True, null=True)),
                ('most_recent_update', models.DateTimeField(blank=True, null=True)),
                ('most_recent_update_status', models.CharField(blank=True, max_length=2500, null=True)),
                ('most_recent_update_time_taken_millis', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='createddashboard_dashboardwidgetsummarylog_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modifieddashboard_dashboardwidgetsummarylog_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChartMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Inactive'), (2, 'Active')], db_index=True, default=2)),
                ('server_created_on', models.DateTimeField(auto_now_add=True)),
                ('server_modified_on', models.DateTimeField(auto_now=True)),
                ('sync_status', models.PositiveIntegerField(default=2)),
                ('chart_type', models.IntegerField(blank=True, choices=[(1, 'Column Chart'), (2, 'Pie Chart'), (3, 'Table Chart'), (4, 'Bar Chart'), (5, 'Column Stack'), (6, 'Bar Stack')], help_text='1=Column Chart, 2=Pie Chart, 3=Table Chart, 4=Bar Chart, 5=Column Stack, 6=Bar Stack', null=True)),
                ('chart_slug', models.CharField(blank=True, max_length=500, null=True, unique=True)),
                ('page_slug', models.CharField(blank=True, max_length=500, null=True)),
                ('chart_title', models.CharField(blank=True, max_length=500, null=True)),
                ('vertical_axis_title', models.CharField(blank=True, max_length=200, null=True)),
                ('horizontal_axis_title', models.CharField(blank=True, max_length=200, null=True)),
                ('chart_note', models.TextField(blank=True, null=True)),
                ('chart_tooltip', models.TextField(blank=True, null=True)),
                ('chart_height', models.TextField(blank=True, help_text='Chart height in pixel or %', null=True)),
                ('click_handler', models.JSONField(blank=True, help_text='json text to set the handler options: {on_click_handler:function-name, url_template:url with placeholders for chart element(bar/column) key value', null=True)),
                ('chart_options', models.JSONField(blank=True, help_text='json text to set the chart options', null=True)),
                ('div_class', models.TextField(blank=True, help_text='div class name to be used for the chart container - ex:col-md-6, col-md-12 etc', null=True)),
                ('chart_query', models.JSONField(blank=True, help_text='sql query and related filter details as json - with keys sqlquery, filters and etc', null=True)),
                ('display_order', models.IntegerField(blank=True, help_text='order in which the charts have to be displayed', null=True)),
                ('filter_info', models.JSONField(blank=True, help_text='report filters meta data in json format', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='createddashboard_chartmeta_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modifieddashboard_chartmeta_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Chart Meta',
            },
        ),
    ]
