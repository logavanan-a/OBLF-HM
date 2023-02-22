from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
import uuid
import datetime
from django.core.validators import RegexValidator
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




class BaseContent(models.Model):
    ACTIVE_CHOICES = ((1, 'Inactive'), (2, 'Active'),)
    uuid = models.CharField(editable=False, unique=True,
                            null=True, blank=True, max_length=200)
    status = models.PositiveIntegerField(
        choices=ACTIVE_CHOICES, default=2, db_index=True)
    server_created_on = models.DateTimeField(auto_now_add=True)
    server_modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', null=True, blank=True,)
    modified_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', null=True, blank=True,)
    sync_status = models.PositiveIntegerField(default=2)

    class Meta:
        abstract = True


class MasterLookup(BaseContent):
    name = models.CharField(max_length=150, blank=False,
                            null=False, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    


class AppContent(BaseContent):
    app_created_on = models.DateField(blank=True, null=True)


class State(BaseContent):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=2, blank=True, null=True)
    parent_id=models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "State"

    def __str__(self):
        return self.name


class District(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=2, blank=True, null=True)
    state = models.ForeignKey(
        State, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [['name', 'state']]
        verbose_name_plural = "District"

    def __str__(self):
        return self.name


class Taluk(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=2, blank=True, null=True)
    district = models.ForeignKey(
        District, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [['name', 'district']]
        verbose_name_plural = "Taluk"

    def __str__(self):
        return self.name


class PHC(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    taluk = models.ForeignKey(
        Taluk, on_delete=models.DO_NOTHING)
    
    class Meta:
        unique_together = [['name', 'taluk']]
        verbose_name_plural = "PHC"

    def __str__(self):
        return self.name

class Subcenter(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=2, blank=True, null=True)
    phc = models.ForeignKey(
        PHC, on_delete=models.DO_NOTHING)

    
    def __str__(self):
        return self.name


class Village(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    subcenter = models.ForeignKey(
        Subcenter, on_delete=models.DO_NOTHING, blank=True, null=True)
    class Meta:
        unique_together = [['name', 'subcenter']]
        verbose_name_plural = "Village"
        ordering = ["subcenter"]

    def __str__(self):
        return self.name

class Comorbid(BaseContent):
    name = models.CharField(max_length=150)
    patient_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Comorbid"

    def __str__(self):
        return self.name

        
class Category(BaseContent):
    name = models.CharField(max_length=200)
    parent_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class MedicinesReportCategory(BaseContent):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Medicines(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    category_id = models.IntegerField(null=True, blank=True)
    medicine_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Medicines"

    def __str__(self):
        return self.name

    def get_no_of_units(self):
        from health_management.models import MedicineStock, DrugDispensation, Prescription
        from django.db.models import Sum
        medicine = MedicineStock.objects.filter(medicine=self)
        medicine_stock_totals = medicine.aggregate(sum=Sum('no_of_units')).get('sum')
        drug_dispensation = DrugDispensation.objects.filter(medicine=self)
        drug_dispensation_total = drug_dispensation.aggregate(sum=Sum('units_dispensed')).get('sum')
        prescription = Prescription.objects.filter(medicines=self)
        prescription_total = prescription.aggregate(sum=Sum('qty')).get('sum')
        if drug_dispensation_total == None:
            drug_dispensation_total = 0
        if medicine_stock_totals == None:
            medicine_stock_totals = 0
        if prescription_total == None:
            prescription_total = 0
        opening_stock_total = abs(int(medicine_stock_totals) - int(drug_dispensation_total)) - int(prescription_total)
        return opening_stock_total

class Dosage(BaseContent):
    name = models.CharField(max_length=200)
    value = models.FloatField(blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Dosage"
    
    def __str__(self):
        return self.name

    







    

    
