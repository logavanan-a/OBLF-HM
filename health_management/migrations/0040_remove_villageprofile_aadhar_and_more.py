# Generated by Django 4.1.7 on 2023-04-03 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health_management', '0039_rename_treatment_uuid_diagnosis_patient_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='villageprofile',
            name='aadhar',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='age',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='alcohol',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='ayushman_bharath_card',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='ayushman_bharath_card_no',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='bmi',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='both',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='bp_med_1',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='bp_med_2',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='bp_med_3',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='code',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='consultation',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='daily_wage_loss',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='date',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='dbp',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='detected_by',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='detected_since',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='diagnosis',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='diagnostics',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='dm',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='dm_med_1',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='dm_med_2',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='facility_1',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='facility_2',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='facility_3',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='family_history',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='fbs',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='food',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='head_of_the_family',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='health_card',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='house_hold',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='htn',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='individual',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='informal_fees',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='medicine_charges',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='name_of_anm',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='name_of_cho',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='name_of_flhw',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='name_of_mo',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='name_of_the_asha',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='ncd_treatment',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='non_ncd_treatment',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='on_treatment',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='opportunity_cost',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='past_history',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='phone_no',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='phone_no_of_anm',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='phone_no_of_cho',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='phone_no_of_flhw',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='phone_no_of_mo',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='physician_visit_in_last_6_months',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='ppbs',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='ration_card_no',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='ration_card_no_type',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='rbs',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='resident_in_the_village_since_last_6_month',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='sbp',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='smoking',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='source_of_treatment',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='statins',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='tobacco',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='total_direct_cost',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='total_indirect_cost',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='travelling',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='voter_id',
        ),
        migrations.RemoveField(
            model_name='villageprofile',
            name='weight',
        ),
    ]