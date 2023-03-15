from django.contrib import admin
from .models import *
from .admin import *

# Register your models here.

admin.site.site_url = '/list/userprofile/'

@admin.register(Patients)
class PatientsAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'village', 'uuid', 'patient_id', 'user_uuid', 'dob', 'age', 'gender', 'phone_number', 'image',
     'height', 'weight', 'door_no', 'seq_no', 'patient_visit_type', 'fee_status', 
     'fee_paid', 'fee_date', 'registered_date', 'last_visit_date', 'server_created_on', 'server_modified_on', 'status']
    fields = ['name', 'village', 'uuid', 'patient_id', 'user_uuid', 'dob', 'age', 'gender', 'phone_number', 'image',
     'height', 'weight', 'door_no', 'seq_no', 'patient_visit_type', 'fee_status',
     'fee_paid', 'fee_date', 'registered_date', 'last_visit_date', 'status']
    search_fields = ['name', 'village__name', 'uuid', 'patient_id', 'user_uuid']
    list_per_page = 15

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patient_visit_type":
            kwargs["queryset"] = MasterLookup.objects.filter(
                parent__name='patient_visit_type')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Treatments)
class TreatmentsAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['uuid', 'user_uuid', 'patient_uuid', 'visit_date', 'bp_sys1', 'bp_non_sys1', 'bp_sys2', 'bp_non_sys2',
     'bp_sys3', 'bp_non_sys3', 'fbs', 'pp', 'random', 'weight', 
     'bmi', 'symptoms', 'remarks', 'hyper_diabetic', 'co_morbid_ids', 'co_morbid_names',
     'is_alcoholic', 'is_tobacco', 'is_smoker', 'server_created_on', 'server_modified_on', 'status']
    fields = ['uuid', 'user_uuid', 'patient_uuid', 'visit_date', 'bp_sys1', 'bp_non_sys1', 'bp_sys2', 'bp_non_sys2',
     'bp_sys3', 'bp_non_sys3', 'fbs', 'pp', 'random', 'weight', 
     'bmi', 'symptoms', 'remarks', 'hyper_diabetic', 'co_morbid_ids', 'co_morbid_names',
     'is_alcoholic', 'is_tobacco', 'is_smoker', 'status']
    search_fields = ['uuid', 'user_uuid', 'patient_uuid']
    date_hierarchy = 'visit_date'
    list_per_page = 15



@admin.register(Prescription)
class PrescriptionAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['medicines', 'uuid', 'user_uuid', 'patient_uuid', 'treatment_uuid',
    'dosage', 'no_of_days', 'medicine_type', 'qty', 'server_created_on', 'server_modified_on', 'status']
    fields = ['medicines', 'user_uuid', 'uuid', 'patient_uuid', 'treatment_uuid',
    'dosage', 'no_of_days', 'medicine_type', 'qty', 'status']
    search_fields = ['medicines__name','uuid', 'user_uuid', 'patient_uuid', 'treatment_uuid']
    list_per_page = 15

@admin.register(Diagnosis)
class DiagnosisAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['ndc', 'uuid', 'user_uuid', 'patient_uuid', 'detected_by', 'source_treatment',
    'years', 'server_created_on', 'server_modified_on', 'status']
    fields = ['ndc', 'uuid', 'user_uuid', 'patient_uuid', 'detected_by', 'source_treatment',
    'years', 'status']
    search_fields = ['ndc__name', 'uuid', 'user_uuid', 'patient_uuid']
    list_per_page = 15

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ndc":
            kwargs["queryset"] = MasterLookup.objects.filter(
                parent__name='ndcs')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Scanned_Report)
class Scanned_ReportAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['title', 'uuid', 'user_uuid', 'patient_uuid', 'image_path',
    'captured_date', 'server_created_on', 'server_modified_on', 'status']
    fields = ['title', 'uuid', 'user_uuid', 'patient_uuid', 'image_path',
    'captured_date', 'status']
    search_fields = ['title', 'uuid', 'user_uuid', 'patient_uuid']
    list_per_page = 15

@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ('uuid', 'user', 'phone_no', 'villages', 
    'user_type', 'server_created_on', 'server_modified_on', 'status')
    fields = ['uuid', 'user', 'village', 'phone_no',
    'user_type', 'status']
    search_fields = ['name', 'user__username', 'village__name', 'uuid']
    list_per_page = 15

    def villages(self, instance):
        return [villages.name for villages in instance.village.all()]

    

@admin.register(HomeVisit)
class HomeVisitAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['uuid', 'patient_uuid', 'user_uuid',
    'home_vist', 'image_location', 'response_location', 'response_datetime', 'image', 'server_created_on', 'server_modified_on', 'status']
    fields = ['uuid', 'image_location', 'patient_uuid', 'user_uuid',
    'home_vist', 'response_location', 'response_datetime',  'image', 'status']
    search_fields = ['uuid', 'patient_uuid', 'user_uuid']
    list_per_page = 15


@admin.register(MedicineStock)
class MedicineStockAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['medicine', 'date_of_creation', 'unit_price', 'no_of_units',
     'opening_stock', 'closing_stock', 'created_by', 'modified_by', 'server_created_on', 'server_modified_on', 'status']
    fields = ['medicine', 'date_of_creation', 'unit_price', 'no_of_units',
     'opening_stock', 'closing_stock', 'status']
    search_fields = ['medicine__name']
    list_per_page = 15

@admin.register(DrugDispensation)
class DrugDispensationAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['medicine', 'village', 'units_dispensed',
     'date_of_dispensation', 'server_created_on', 'server_modified_on', 'status']
    fields = ['medicine', 'village', 'units_dispensed',
     'date_of_dispensation', 'status']
    search_fields = ['medicine__name', 'village__name']
    list_per_page = 15


# class VillageProfileResource(resources.ModelResource):

#     class Meta:
#         model = VillageProfile

#     def skip_row(self, instance, original):
#         # try:
#         village_profile_code = VillageProfile.objects.filter(code=instance.code).exists()
#         if village_profile_code:
#             return True
        #     else:
        #         village_import = Patients.objects.get(patient_id=instance.code)
        # except Patients.DoesNotExist:
        #     village_import = None
    # if village_import is None:
    #     return True
            

@admin.register(VillageProfile)
class VillageProfileAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['village', 'house_hold', 'individual', 'code', 'name', 'head_of_the_family','age','gender','phone_no','resident_in_the_village_since_last_6_month','name_of_the_asha',
    'name_of_flhw','phone_no_of_flhw','name_of_anm','phone_no_of_anm','name_of_cho','phone_no_of_cho','name_of_mo',
    'phone_no_of_mo','voter_id','aadhar','health_card','ayushman_bharath_card','ayushman_bharath_card_no','ration_card_no',
    'ration_card_no_type','htn','dm','both','detected_by','detected_since','on_treatment','physician_visit_in_last_6_months',
    'facility','facility_1','facility_2','facility_3','medicine_charges','consultation','diagnostics','informal_fees',
    'total_direct_cost','food','travelling','total_indirect_cost','daily_wage_loss','opportunity_cost','bp_med_1',
    'bp_med_2','bp_med_3','dm_med_1','dm_med_2','statins','tobacco','alcohol','smoking','family_history',
    'date','source_of_treatment','height','weight','bmi','sbp','dbp','fbs','ppbs','rbs','diagnosis','ncd_treatment',
    'non_ncd_treatment','past_history','remarks', 'server_created_on', 'server_modified_on', 'status']
    fields = ['village','house_hold', 'individual', 'code', 'name', 'head_of_the_family','age','gender','phone_no','resident_in_the_village_since_last_6_month','name_of_the_asha',
    'name_of_flhw','phone_no_of_flhw','name_of_anm','phone_no_of_anm','name_of_cho','phone_no_of_cho','name_of_mo',
    'phone_no_of_mo','voter_id','aadhar','health_card','ayushman_bharath_card','ayushman_bharath_card_no','ration_card_no',
    'ration_card_no_type','htn','dm','both','detected_by','detected_since','on_treatment','physician_visit_in_last_6_months',
    'facility','facility_1','facility_2','facility_3','medicine_charges','consultation','diagnostics','informal_fees',
    'total_direct_cost','food','travelling','total_indirect_cost','daily_wage_loss','opportunity_cost','bp_med_1',
    'bp_med_2','bp_med_3','dm_med_1','dm_med_2','statins','tobacco','alcohol','smoking','family_history',
    'date','source_of_treatment','height','weight','bmi','sbp','dbp','fbs','ppbs','rbs','diagnosis','ncd_treatment',
    'non_ncd_treatment','past_history','remarks', 'status']
    search_fields = ['village__name']
    list_per_page = 15

    # resource_class = VillageProfileResource




















