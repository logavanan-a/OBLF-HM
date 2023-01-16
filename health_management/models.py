from django.db import models
from django.db import models
from application_masters.models import *
import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

phone_regex = RegexValidator(
    regex=r'\d{10}$', message="Phone number must be 10 digits") 

class Patients(BaseContent):
    GENDER_CHOICE = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other')
        )
    uuid = models.CharField(max_length=150, blank=True, null=True)
    patient_id = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150)
    dob = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICE, blank=True, null=True)
    village = models.ForeignKey(
        Village, on_delete=models.DO_NOTHING, blank=True, null=True)
    phone_number = models.CharField(max_length=10, validators=[
                                    phone_regex], unique=False, blank=True, null=True)
    image = models.FileField(
        upload_to='patients_image/%y/%m/%d/', blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    subcenter_id = models.PositiveIntegerField(blank=True, null=True)
    door_no = models.CharField(max_length=150, null=True, blank=True)
    seq_no = models.CharField(max_length=150, null=True, blank=True)
    patient_visit_type = models.ForeignKey(
        MasterLookup, on_delete=models.DO_NOTHING, null=True, blank=True)
    fee_status = models.PositiveIntegerField(null=True, blank=True)
    fee_paid = models.PositiveIntegerField(null=True, blank=True)
    fee_date = models.DateTimeField(null=True, blank=True)
    registered_date = models.DateTimeField(null=True, blank=True)
    last_visit_date = models.DateTimeField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Patients"
    
    def __str__(self):
        return self.name

    def get_health_worker(self):
        try:
            health_worker = UserProfile.objects.get(village=self.village, user_type=1)
        except ObjectDoesNotExist:
            health_worker = None
        return health_worker




class Treatments(BaseContent):
    SMOKER_CHOICES = (
    (0, 'No'),
    (1, 'Yes')
    )
    uuid = models.CharField(max_length=150, null=True, blank=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True)
    visit_date = models.DateTimeField(null=True, blank=True)
    bp_sys1 = models.CharField(max_length=150, null=True, blank=True)
    bp_non_sys1 = models.CharField(max_length=150, null=True, blank=True)
    bp_sys2 = models.CharField(max_length=150, null=True, blank=True)
    bp_non_sys2 = models.CharField(max_length=150, null=True, blank=True)
    bp_sys3 = models.CharField(max_length=150, null=True, blank=True)
    bp_non_sys3 = models.CharField(max_length=150, null=True, blank=True)
    fbs = models.CharField(max_length=150, null=True, blank=True)
    pp = models.CharField(max_length=150, null=True, blank=True)
    random = models.CharField(max_length=150, null=True, blank=True)
    weight = models.CharField(max_length=150, null=True, blank=True)
    bmi = models.CharField(max_length=150, null=True, blank=True)
    symptoms = models.CharField(max_length=150, null=True, blank=True)
    remarks = models.CharField(max_length=150, null=True, blank=True)
    hyper_diabetic = models.PositiveIntegerField(null=True, blank=True)
    co_morbid_ids = models.CharField(max_length=150, null=True, blank=True)
    co_morbid_names = models.CharField(max_length=150, null=True, blank=True)
    is_alcoholic = models.IntegerField(null=True, blank=True)
    is_tobacco = models.IntegerField(null=True, blank=True)
    is_smoker = models.IntegerField(choices = SMOKER_CHOICES, null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Treatments"






class Prescription(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True)
    treatment_uuid = models.CharField(max_length=150, null=True, blank=True)
    medicines = models.ForeignKey(
        Medicines, on_delete=models.DO_NOTHING)
    dosage = models.ForeignKey(Dosage, on_delete=models.DO_NOTHING,blank =True,null =True)
    no_of_days = models.IntegerField(null=True, blank=True)
    medicine_type = models.CharField(max_length=150, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Prescription"

    def __str__(self):
        return self.medicines.name
    
    def get_user_uuid(self):
        try:
            patients_list=Patients.objects.get(uuid=self.patient_uuid)
        except ObjectDoesNotExist:
            patients_list = None
        return patients_list
    
    def get_treatment_uuid(self):
        try:
            treatments_list=Treatments.objects.get(uuid=self.treatment_uuid)
        except ObjectDoesNotExist:
            treatments_list = None
        return treatments_list


class Diagnosis(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True)
    treatment_uuid = models.CharField(max_length=150, null=True, blank=True)
    ndc = models.ForeignKey(
        MasterLookup, on_delete=models.DO_NOTHING)
    source_treatment = models.IntegerField(null=True, blank=True)
    detected_by = models.IntegerField(null=True, blank=True)
    years = models.CharField(max_length=150, null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Diagnosis"






class Scanned_Report(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    image_path = models.CharField(max_length=150, null=True, blank=True)
    captured_date = models.DateTimeField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Scanned Report"


class UserProfile(BaseContent):
    USER_TYPE_CHOICES = ((1, 'Health worker'), (2, 'Doctor'))
    uuid = models.CharField(max_length=200,unique =True, default=uuid.uuid4,null=True)
    name = models.CharField(blank=True,null=True,max_length=450)
    email = models.CharField(blank=True,null=True,max_length=50)
    phone_no = models.CharField(max_length=150, unique=True, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    village = models.ForeignKey(
        Village, on_delete=models.DO_NOTHING)
    user_type= models.PositiveIntegerField(choices=USER_TYPE_CHOICES,default=0, db_index=True)
    def __str__(self):
        return self.user.username

class HomeVisit(BaseContent):
    VISIT_TYPE_CHOICES = ((1, 'No'), (2, 'Yes'))
    uuid = models.CharField(max_length=150, null=True, blank=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True)
    home_vist = models.PositiveIntegerField(choices=VISIT_TYPE_CHOICES, default=0)
    response_location = models.CharField(max_length=150, null=True, blank=True)
    response_datetime = models.DateTimeField(null=True, blank=True)
    image = models.FileField(
        upload_to='home_visit_image/%y/%m/%d/', blank=True, null=True)

class MedicineStock(BaseContent):
    medicine = models.ForeignKey(Medicines, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_of_creation = models.DateField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(null=True, blank=True)
    no_of_units = models.PositiveIntegerField(null=True, blank=True)
    opening_stock = models.IntegerField(null=True, blank=True)
    closing_stock = models.IntegerField(null=True, blank=True)


class DrugDispensation(BaseContent):
    medicine = models.ForeignKey(Medicines, on_delete=models.DO_NOTHING, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.DO_NOTHING)
    units_dispensed = models.PositiveIntegerField(null=True, blank=True)
    date_of_dispensation = models.DateField(null=True, blank=True)

    







