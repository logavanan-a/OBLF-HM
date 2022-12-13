from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'village', 'uuid', 'patient_id', 'dob', 'age', 'gender', 'phone_number', 'image',
     'height', 'weight', 'door_no', 'patient_visit_type', 'fee_status', 
     'fee_paid', 'fee_date', 'registered_date', 'last_visit_date', 'status']
    fields = ['name', 'village', 'uuid', 'patient_id', 'dob', 'age', 'gender', 'phone_number', 'image',
     'height', 'weight', 'door_no', 'patient_visit_type', 'fee_status',
     'fee_paid', 'fee_date', 'registered_date', 'last_visit_date', 'status']
    search_fields = ['name', 'village__name']
    list_per_page = 15

@admin.register(Treatments)
class TreatmentsAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'patient_uuid', 'visit_date', 'bp_sys1', 'bp_non_sys1', 'bp_sys2', 'bp_non_sys2',
     'bp_sys3', 'bp_non_sys3', 'fbs', 'pp', 'random', 'weight', 
     'bmi', 'symptoms', 'remarks', 'hyper_diabetic', 'co_morbid_ids', 'co_morbid_names',
     'is_alcoholic', 'is_tobacco', 'is_smoker', 'status']
    fields = ['uuid', 'patient_uuid', 'visit_date', 'bp_sys1', 'bp_non_sys1', 'bp_sys2', 'bp_non_sys2',
     'bp_sys3', 'bp_non_sys3', 'fbs', 'pp', 'random', 'weight', 
     'bmi', 'symptoms', 'remarks', 'hyper_diabetic', 'co_morbid_ids', 'co_morbid_names',
     'is_alcoholic', 'is_tobacco', 'is_smoker', 'status']
    list_per_page = 15




@admin.register(Medicines)
class MedicinesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'types', 'category_id', 'status']
    fields = ['name', 'code', 'types', 'category_id', 'status']
    search_fields = ['name']
    list_per_page = 15

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medicines', 'uuid', 'patient_uuid', 'treatment_uuid',
    'dosage', 'no_of_days', 'medicine_type', 'qty', 'status']
    fields = ['medicines', 'uuid', 'patient_uuid', 'treatment_uuid',
    'dosage', 'no_of_days', 'medicine_type', 'qty', 'status']
    search_fields = ['medicines__name']
    list_per_page = 15

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['ndc', 'uuid', 'treatment_uuid', 'detected_by', 'source_treatment',
    'years', 'status']
    fields = ['ndc', 'uuid', 'treatment_uuid', 'detected_by', 'source_treatment',
    'years', 'status']
    search_fields = ['ndc__name']
    list_per_page = 15

@admin.register(Scanned_Report)
class Scanned_ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'uuid', 'patient_uuid', 'image_path',
    'captured_date', 'status']
    fields = ['title', 'uuid', 'patient_uuid', 'image_path',
    'captured_date', 'status']
    search_fields = ['title']
    list_per_page = 15

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'email', 'user', 'village',
    'user_type', 'status']
    fields = ['uuid', 'name', 'user', 'email', 'village',
    'user_type', 'status']
    search_fields = ['name', 'user__username', 'village__name']
    list_per_page = 15


















