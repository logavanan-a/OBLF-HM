from import_export import resources
from django.contrib import admin
from .models import *



# # Register your models here.


@admin.register(MasterLookup)
class MasterLookupAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    fields = ['name', 'parent', 'order']
    search_fields = ['name']
    list_per_page = 15


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    fields = ['name', 'status']
    search_fields = ['name']
    list_per_page = 15


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'status']
    fields = ['name', 'state', 'status']
    search_fields = ['name', 'state__name']
    list_per_page = 15


@admin.register(Taluk)
class TalukAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'status']
    fields = ['name', 'district', 'status']
    search_fields = ['name', 'district__name']
    list_per_page = 15


@admin.register(PHC)
class PHCAdmin(admin.ModelAdmin):
    list_display = ['name', 'taluk', 'phc_code', 'status']
    fields = ['name', 'taluk', 'phc_code', 'status']
    search_fields = ['name', 'taluk__name', 'code']
    list_per_page = 15

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ['name', 'phc', 'code', 'status']
    fields = ['name', 'phc', 'code', 'status']
    search_fields = ['name', 'phc__name', 'code']
    list_per_page = 15