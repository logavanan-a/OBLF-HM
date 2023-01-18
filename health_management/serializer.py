import imp
from rest_framework import serializers
from application_masters.models import *
from health_management.models import *

from django.contrib.auth import authenticate,login,logout
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from rest_framework.response import Response

class StateSerializers(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class DistrictSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class TalukSerializers(serializers.ModelSerializer):
    class Meta:
        model = Taluk
        fields = '__all__'


class PHCSerializers(serializers.ModelSerializer):
    class Meta:
        model = PHC
        fields = '__all__'

class SubcenterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subcenter
        fields = '__all__'

class MasterLookupSerializers(serializers.ModelSerializer):
    class Meta:
        model = MasterLookup
        exclude = ['parent', 'order']
        

class VillageSerializers(serializers.ModelSerializer):
    subcenter_id = serializers.CharField(source='subcenter.id')
    class Meta:
        model = Village
        exclude = ['subcenter']
        


class MedicineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields = '__all__'

class ComorbidSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comorbid
        exclude = ['patient_id']

class DosageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dosage
        fields = '__all__'

class PatientSerializers(serializers.ModelSerializer):
    village_id = serializers.CharField(source='village.id', required=False,allow_blank=True)
    subcenter_id = serializers.CharField(source='village.subcenter.id', required=False,allow_blank=True)
    phc_id = serializers.CharField(source='village.subcenter.phc.id', required=False,allow_blank=True)
    # taluk_id = serializers.CharField(source='village.phc.taluk.id')
    # district_id = serializers.CharField(source='village.phc.taluk.district.id')
    class Meta:
        model = Patients
        exclude = ['village']

class TreatmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Treatments
        fields = '__all__'

class PrescriptionSerializers(serializers.ModelSerializer):
    medicine_id = serializers.CharField(source='medicines.id')
    class Meta:
        model = Prescription
        exclude = ['medicines']

class HomeVisitSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomeVisit
        fields = '__all__'


class DiagnosisSerializers(serializers.ModelSerializer):
    ndc_id = serializers.CharField(source='ndc.id')
    class Meta:
        model = Diagnosis
        exclude = ['ndc']

class ScannedReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Scanned_Report
        fields = '__all__'

class UserProfileSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    village_id = serializers.CharField(source='village.id')
    subcenter_id = serializers.CharField(source='village.subcenter.id')
    phc_id = serializers.CharField(source='village.subcenter.phc.id')
    class Meta:
        model = UserProfile
        exclude = ['user', 'village']
