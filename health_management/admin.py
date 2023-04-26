from django.contrib import admin
from .models import *
from .admin import *
import uuid
# Register your models here.

admin.site.site_url = '/list/userprofile/'

class PatientsResource(resources.ModelResource):
    class Meta:
        model = Patients

@admin.register(Patients)
class PatientsAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'village', 'uuid', 'patient_id', 'user_uuid', 'dob', 'age', 'gender', 'phone_number', 'image',
     'height', 'weight', 'door_no', 'seq_no', 'patient_visit_type', 'fee_status', 
     'fee_paid', 'fee_date', 'registered_date', 'last_visit_date', 'server_created_on', 'server_modified_on', 'status']
    fields = ['name', 'village', 'uuid', 'patient_id', 'user_uuid', 'dob', 'age', 'gender', 'phone_number', 'image',
     'height', 'weight', 'door_no', 'seq_no', 'patient_visit_type', 'fee_status',
     'fee_paid', 'fee_date', 'registered_date', 'last_visit_date', 'status']
    search_fields = ['name', 'uuid', 'patient_id', 'user_uuid']
    list_filter = ['village' ]

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
     'is_alcoholic', 'is_tobacco', 'is_smoker', 'is_controlled', 'server_created_on', 'server_modified_on', 'status']
    fields = ['uuid', 'user_uuid', 'patient_uuid', 'visit_date', 'bp_sys1', 'bp_non_sys1', 'bp_sys2', 'bp_non_sys2',
     'bp_sys3', 'bp_non_sys3', 'fbs', 'pp', 'random', 'weight', 
     'bmi', 'symptoms', 'remarks', 'hyper_diabetic', 'co_morbid_ids', 'co_morbid_names',
     'is_alcoholic', 'is_tobacco', 'is_smoker', 'is_controlled', 'status']
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
    list_filter = ['medicines', ]
    list_per_page = 15

@admin.register(Diagnosis)
class DiagnosisAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['ndc', 'uuid', 'user_uuid', 'patient_uuid', 'detected_by', 'source_treatment',
    'years', 'server_created_on', 'server_modified_on', 'status']
    fields = ['ndc', 'uuid', 'user_uuid', 'patient_uuid', 'detected_by', 'source_treatment',
    'years', 'status']
    search_fields = ['ndc__name', 'uuid', 'user_uuid', 'patient_uuid']
    list_filter = ['ndc' ]
    list_per_page = 15

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ndc":
            kwargs["queryset"] = MasterLookup.objects.filter(
                status=2,parent__name='ndcs')
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
    search_fields = ['user__username', 'village__name', 'uuid']
    list_per_page = 15

    def villages(self, instance):
        return [villages.name for villages in instance.village.filter()]

    

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

#     def before_save_instance(self, instance, using_transactions, dry_run):
#         curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
#         user_id=UserProfile.objects.get(village=instance.village)
#         uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
#         obj, created  = Patients.objects.update_or_create(patient_id=instance.patient_id,
#         defaults={"uuid":uuid_id, "user_uuid":user_id.uuid, "name":instance.name,"age":instance.age,
#         "gender":instance.gender, "village":instance.village, "phone_number":instance.phone_number,
#         "image":instance.image,"subcenter_id":instance.subcenter_id, "door_no":instance.door_no,
#         "seq_no":instance.seq_no})
#         obj.save()
#         # instance.
#         # Patients=Patients.objects.filter(status=2).values_list('patient_id', flat=True)
#         # if dry_run:
#         #     print('dbvbdb')
#         # else:
        #     print('none')


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
    list_display = ['name', 'door_no', 'seq_no', 'patient_id', 'village', 'dob', 'age', 'gender',
     'phone_number', 'image', 'subcenter_id', 'server_created_on', 'server_modified_on', 'data_migration', 'status']
    fields = ['name', 'patient_id', 'village', 'dob', 'age', 'gender',
     'phone_number', 'image', 'subcenter_id', 'door_no', 'seq_no', 'data_migration', 'status']
    search_fields = ['patient_id']
    list_filter = ['village' ]
    list_per_page = 15

    # resource_class = VillageProfileResource

@admin.register(ClinicProfile)
class ClinicProfileAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['code', 'htn', 'detected_by_htn', 'detected_since_htn', 'dm', 'detected_by_dm', 'detected_since_dm', 'tobacco',
     'alcohol', 'smoking', 'date', 'weight', 'bmi', 'sbp', 'dbp', 'fbs',
     'ppbs', 'rbs', 'symptoms', 'remarks', 'server_created_on', 
     'server_modified_on', 'status']
    fields = ['code', 'htn', 'detected_by_htn', 'detected_since_htn', 'dm', 'detected_by_dm', 'detected_since_dm', 'tobacco',
     'alcohol', 'smoking', 'date', 'weight', 'bmi', 'sbp', 'dbp', 'fbs',
     'ppbs', 'rbs', 'symptoms', 'remarks', 'status']
    search_fields = ['code']
    list_per_page = 15




















