from import_export import resources
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export.formats import base_formats
from import_export import resources, fields
from import_export.fields import Field



class ImportExportFormat(ImportExportMixin):
    def get_export_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX, base_formats.XLS,)
        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX, base_formats.XLS,)
        return [f for f in formats if f().can_import()]

# # Register your models here.

@admin.register(MasterLookup)
class MasterLookupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'status']
    fields = ['name', 'parent', 'order', 'status']
    search_fields = ['name']
    list_per_page = 15


@admin.register(State)
class StateAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'code',  'parent_id', 'status']
    fields = ['name', 'parent_id', 'code', 'status']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 15


@admin.register(District)
class DistrictAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'code', 'state', 'status']
    fields = ['name', 'code', 'state', 'status']
    search_fields = ['name', 'state__name']
    ordering = ['name']
    list_per_page = 15


@admin.register(Taluk)
class TalukAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'code', 'district', 'status']
    fields = ['name', 'code', 'district', 'status']
    search_fields = ['name', 'district__name']
    ordering = ['name']
    list_per_page = 15


@admin.register(PHC)
class PHCAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'taluk', 'code', 'status']
    fields = ['name', 'taluk', 'code', 'status']
    search_fields = ['name', 'taluk__name', 'code']
    ordering = ['name']
    list_per_page = 15

@admin.register(Subcenter)
class SubcenterAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'phc', 'code', 'status']
    fields = ['name', 'phc', 'code', 'status']
    search_fields = ['name', 'phc__name', 'code']
    ordering = ['name']
    list_per_page = 15

@admin.register(Village)
class VillageAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'subcenter', 'code', 'status']
    fields = ['name', 'subcenter', 'code', 'status']
    search_fields = ['name', 'subcenter__name', 'code']
    ordering = ['name']
    list_per_page = 15


@admin.register(Comorbid)
class ComorbidAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'patient_id', 'status']
    fields = ['name', 'patient_id', 'status']
    search_fields = ['name', 'patient_id']
    ordering = ['name']
    list_per_page = 15

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'parent_id', 'status']
    fields = ['name', 'parent_id', 'status']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 15

@admin.register(MedicinesReportCategory)
class MedicinesReportCategoryAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'status']
    fields = ['name', 'status']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 15

@admin.register(Medicines)
class MedicinesAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'code', 'medicines_type', 'category', 'medicine_id', 'status']
    fields = ['name', 'code', 'medicines_type', 'category', 'medicine_id', 'status']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['category', 'medicines_type', 'medicine_id']
    list_per_page = 15

@admin.register(Dosage)
class DosageAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['name', 'value', 'status']
    fields = ['name', 'value', 'status']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 15

