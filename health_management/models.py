from django.db import models
from django.db import models
from application_masters.models import *
import datetime
from django.db.models import Q

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
        Village, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=10, validators=[
                                    phone_regex], unique=True)
    image = models.FileField(
        upload_to='patients_image/%y/%m/%d/', blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    door_no = models.CharField(max_length=150, null=True, blank=True)
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


class Comorbid(BaseContent):
    name = models.CharField(max_length=150)
    patients = models.ForeignKey(
        Patients, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Comorbid"

    def __str__(self):
        return self.name

    



class Medicines(BaseContent):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    types = models.CharField(max_length=50, blank=True, null=True)
    category_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Medicines"

    def __str__(self):
        return self.name


class Prescription(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True)
    treatment_uuid = models.CharField(max_length=150, null=True, blank=True)
    medicines = models.ForeignKey(
        Medicines, on_delete=models.DO_NOTHING)
    dosage = models.CharField(max_length=150, null=True, blank=True)
    no_of_days = models.IntegerField(null=True, blank=True)
    medicine_type = models.CharField(max_length=150, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Prescription"

    def __str__(self):
        return self.medicines.name


class Diagnosis(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True)
    treatment_uuid = models.CharField(max_length=150, null=True, blank=True)
    ndc = models.ForeignKey(
        MasterLookup, on_delete=models.DO_NOTHING)
    source_treatment = models.IntegerField(null=True, blank=True)
    detected_by = models.IntegerField(null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
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
    uuid = models.CharField(max_length=200,unique =True,default=uuid.uuid4,null=True)
    name = models.CharField(blank=True,null=True,max_length=450)
    email = models.CharField(blank=True,null=True,max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    village = models.ForeignKey(
        Village, on_delete=models.DO_NOTHING)
    user_type= models.PositiveIntegerField(choices=USER_TYPE_CHOICES,default=0, db_index=True)
    def __str__(self):
        return self.user.username








