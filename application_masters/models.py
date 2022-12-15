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
    parent_id=models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "State"

    def __str__(self):
        return self.name


class District(BaseContent):
    name = models.CharField(max_length=150)
    state = models.ForeignKey(
        State, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [['name', 'state']]
        verbose_name_plural = "District"

    def __str__(self):
        return self.name


class Taluk(BaseContent):
    name = models.CharField(max_length=150)
    district = models.ForeignKey(
        District, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [['name', 'district']]
        verbose_name_plural = "Taluk"

    def __str__(self):
        return self.name


class PHC(BaseContent):
    name = models.CharField(max_length=150)
    phc_code = models.CharField(max_length=50, blank=True, null=True)
    taluk = models.ForeignKey(
        Taluk, on_delete=models.DO_NOTHING)
    
    class Meta:
        unique_together = [['name', 'taluk']]
        verbose_name_plural = "PHC"

    def __str__(self):
        return self.name

class Village(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    phc = models.ForeignKey(
        PHC, on_delete=models.DO_NOTHING)
    
    class Meta:
        unique_together = [['name', 'phc']]
        verbose_name_plural = "Village"

    def __str__(self):
        return self.name

class Comorbid(BaseContent):
    name = models.CharField(max_length=150)
    patient_id = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Comorbid"

    def __str__(self):
        return self.name


class Medicines(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    category_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Medicines"

    def __str__(self):
        return self.name

class Dosage(BaseContent):
    name = models.CharField(max_length=200)
    value = models.FloatField(blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Dosage"
    
    def __str__(self):
        return self.name

    







    

    
