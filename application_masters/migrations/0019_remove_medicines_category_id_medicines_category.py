# Generated by Django 4.1.7 on 2023-03-14 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application_masters', '0018_alter_appcontent_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicines',
            name='category_id',
        ),
        migrations.AddField(
            model_name='medicines',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application_masters.category'),
        ),
    ]
