# Generated by Django 4.1.7 on 2023-03-14 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application_masters', '0017_auto_20230222_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcontent',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appcontent',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comorbid',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comorbid',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='district',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='district',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dosage',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dosage',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='masterlookup',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='masterlookup',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicines',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicines',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicinesreportcategory',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicinesreportcategory',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='phc',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='phc',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='state',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='state',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subcenter',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subcenter',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taluk',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taluk',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='village',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='village',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL),
        ),
    ]