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

class MasterLookupSerializers(serializers.ModelSerializer):
    class Meta:
        model = MasterLookup
        fields = '__all__'

class VillageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'

class MedicineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields = '__all__'

class ComorbidSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comorbid
        fields = '__all__'

class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'

class TreatmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Treatments
        fields = '__all__'

class PrescriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class DiagnosisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class ScannedReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Scanned_Report
        fields = '__all__'

class UserProfileSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = UserProfile
        fields = '__all__'
