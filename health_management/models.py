from django.db import models
from django.db import models
from application_masters.models import *
import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
# import uuid

# Create your models here.

phone_regex = RegexValidator(
    regex=r'\d{10}$', message="Phone number must be 10 digits") 

class Patients(BaseContent):
    # default=uuid.uuid4,
    GENDER_CHOICE = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other')
        )
    uuid = models.CharField(max_length=150, unique =True, blank=True, null=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_id = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=150)
    dob = models.DateField(blank=True, null=True)
    # age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICE, blank=True, null=True)
    village = models.ForeignKey(
        Village, on_delete=models.DO_NOTHING, blank=True, null=True)
    phone_number = models.CharField(max_length=150, validators=[
                                    phone_regex], unique=False, blank=True, null=True)
    image = models.FileField(
        upload_to='patients_image/%y/%m/%d/', blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    # weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    subcenter_id = models.PositiveIntegerField(blank=True, null=True)
    door_no = models.CharField(max_length=150, null=True, blank=True)
    seq_no = models.CharField(max_length=150, null=True, blank=True)
    patient_visit_type = models.ForeignKey(
        MasterLookup, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    registered_date = models.DateTimeField(null=True, blank=True)
    # last_visit_date = models.DateTimeField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Patients"
        ordering = ["village"]

    
    def __str__(self):
        return self.name

    def get_health_worker(self):
        try:
            health_worker = UserProfile.objects.get(uuid=self.user_uuid, user_type=1)
        except ObjectDoesNotExist:
            health_worker = None
        return health_worker
    
    def get_diagnosis_id(self):
        try:
            patient_ids=Treatments.objects.get(patient_uuid=self.uuid)
            diagnosis_id = Diagnosis.objects.get(treatment_uuid=patient_ids.uuid)
        except ObjectDoesNotExist:
            diagnosis_id = None
        return diagnosis_id

    def calculate_age(self):
        from datetime import date
        try: 
            today = date.today()
            today_dob = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        except:
            today_dob = None
        return today_dob

    def get_prescription_uuid(self):
        try:
            prescription_values=Prescription.objects.filter(patient_uuid=self.uuid).first()
        except ObjectDoesNotExist:
            prescription_values=None
        return prescription_values
    


class Treatments(BaseContent):
    SMOKER_CONTROLLED = (
    (0, 'No'),
    (1, 'Yes')
    )
    SOURCE_TREATEMENT_CHOICE = (
    (1, 'CLINIC'),
    (2, 'OUTSIDE'),
    (3, 'C & O'),
    (4, 'NOT')
    )
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    visit_date = models.DateTimeField(null=True, blank=True, db_index=True)
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
    remarks = models.CharField(max_length=500, null=True, blank=True)
    source_treatment = models.IntegerField(choices = SOURCE_TREATEMENT_CHOICE, null=True, blank=True)
    is_controlled = models.IntegerField(choices = SMOKER_CONTROLLED, null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Treatments"

    def get_patients_uuid(self):
        try:
            patients_list=Patients.objects.get(uuid=self.patient_uuid)
        except ObjectDoesNotExist:
            patients_list = None
        return patients_list


class Health(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True, unique =True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, unique =True, null=True, blank=True, db_index=True)
    hyper_diabetic = models.IntegerField(default=0)
    co_morbid_ids = models.CharField(max_length=150, null=True, blank=True)
    co_morbid_names = models.CharField(max_length=500, null=True, blank=True)
    is_alcoholic = models.IntegerField(default=0)
    is_tobacco = models.IntegerField(default=0)
    is_smoker = models.IntegerField(default=0, null=True, blank=True)
    dm_check = models.IntegerField(default=0)
    ht_check = models.IntegerField(default=0)
    dm_status = models.IntegerField(default=0)
    ht_status = models.IntegerField(default=0)
    dm_years = models.DateField(null=True, blank=True)
    ht_years = models.DateField(null=True, blank=True)


    #new
    pdm_year = models.DateField(null=True, blank=True)
    dm_year = models.DateField(null=True, blank=True)
    pht_year = models.DateField(null=True, blank=True)
    ht_year = models.DateField(null=True, blank=True)

    dm_source_treatment = models.IntegerField(default=0)
    ht_source_treatment = models.   IntegerField(default=0)
    pdm_source_treatment = models.IntegerField(default=0)
    pht_source_treatment = models.IntegerField(default=0)

    dm_detected_by = models.IntegerField(default=0)
    ht_detected_by = models.IntegerField(default=0)
    pdm_detected_by = models.IntegerField(default=0)
    pht_detected_by = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.uuid

    def get_pnt_uuid(self):
        try:
            pnt_uuid = Patients.objects.get(uuid=self.patient_uuid)
        except ObjectDoesNotExist:
            pnt_uuid = None
        return pnt_uuid

class PatientComorbids(BaseContent):
    uuid = models.CharField(max_length=150, null=True, blank=True, unique =True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    month_year = models.DateField(null=True, blank=True)
    co_morbid_id = models.IntegerField(null=True, blank=True)




class Prescription(BaseContent):
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    treatment_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
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
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    ndc = models.ForeignKey(
        MasterLookup, on_delete=models.DO_NOTHING)
    source_treatment = models.IntegerField(null=True, blank=True)
    detected_by = models.IntegerField(null=True, blank=True)
    detected_years = models.DateField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Diagnosis"
    
    def get_patients_uuid(self):
        try:
            patients_list=Patients.objects.get(uuid=self.patient_uuid)
        except ObjectDoesNotExist:
            patients_list = None
        return patients_list
    
    def get_health_worker(self):
        try:
            health_worker = UserProfile.objects.get(uuid=self.user_uuid, user_type=1)
        except ObjectDoesNotExist:
            health_worker = None
        return health_worker



class Scanned_Report(BaseContent):
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    image_path = models.CharField(max_length=150, null=True, blank=True)
    captured_date = models.DateTimeField(null=True, blank=True)
    sync_status = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "Scanned Report"


class UserProfile(BaseContent):
    USER_TYPE_CHOICES = ((1, 'Health worker'), (2, 'Doctor'))
    uuid = models.CharField(max_length=200,unique =True, default=uuid.uuid4,null=True, db_index=True)
    phone_no = models.CharField(max_length=150, unique=False, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    village = models.ManyToManyField(Village, blank=True)
    user_type= models.PositiveIntegerField(choices=USER_TYPE_CHOICES,default=0, db_index=True)

    def __str__(self):
        return self.user.username

class HomeVisit(BaseContent):
    VISIT_TYPE_CHOICES = ((1, 'No'), (2, 'Yes'))
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    home_vist = models.PositiveIntegerField(choices=VISIT_TYPE_CHOICES, default=0)
    image_location = models.CharField(max_length=150, null=True, blank=True)
    response_location = models.CharField(max_length=150, null=True, blank=True)
    response_datetime = models.DateTimeField(null=True, blank=True)
    image = models.FileField(
        upload_to='home_visit_image/%y/%m/%d/', blank=True, null=True)

    def get_health_worker(self):
        try:
            health_worker = UserProfile.objects.get(uuid=self.user_uuid, user_type=1)
        except ObjectDoesNotExist:
            health_worker = None
        return health_worker
    
    def get_patient_uuid(self):
        try:
            patients_list=Patients.objects.get(uuid=self.patient_uuid)
        except ObjectDoesNotExist:
            patients_list = None
        return patients_list

class FeePayement(BaseContent):
    uuid = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)
    user_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    patient_uuid = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    fee_status = models.PositiveIntegerField(null=True, blank=True)
    fee_paid = models.PositiveIntegerField(null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
   

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


class VillageProfile(BaseContent):
    GENDER_CHOICE = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other')
        )
    name = models.CharField(max_length=150, null=True, blank=True)
    patient_id = models.CharField(max_length=150, null=True, blank=True, unique=True)
    village = models.ForeignKey(Village, on_delete=models.DO_NOTHING)
    dob = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICE, blank=True, null=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    image = models.FileField(
        upload_to='village_profile_image/%y/%m/%d/', blank=True, null=True)
    subcenter_id = models.CharField(max_length=150, null=True, blank=True)
    door_no = models.CharField(max_length=150, null=True, blank=True)
    seq_no = models.CharField(max_length=150, null=True, blank=True)
    data_migration = models.IntegerField(default=1, null=True, blank=True)
    
class ClinicProfile(BaseContent):
    code = models.CharField(max_length=150, null=True, blank=True)
    htn = models.IntegerField(null=True, blank=True)
    detected_by_htn = models.IntegerField(null=True, blank=True)
    detected_since_htn = models.CharField(max_length=150, null=True, blank=True)
    dm = models.IntegerField(null=True, blank=True)
    detected_by_dm = models.IntegerField(null=True, blank=True)
    detected_since_dm = models.CharField(max_length=150, null=True, blank=True)
    family_history = models.IntegerField(null=True, blank=True)
    tobacco = models.IntegerField(null=True, blank=True)
    alcohol = models.IntegerField(null=True, blank=True)
    smoking = models.IntegerField(null=True, blank=True)
    visit_date = models.DateField(blank=True, null=True)
    source_treatment = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=150, null=True, blank=True)
    weight = models.CharField(max_length=150, null=True, blank=True)
    bmi = models.CharField(max_length=150, null=True, blank=True)
    sbp = models.CharField(max_length=150, null=True, blank=True)
    dbp = models.CharField(max_length=150, null=True, blank=True)
    fbs = models.CharField(max_length=150, null=True, blank=True)
    ppbs = models.CharField(max_length=150, null=True, blank=True)
    rbs = models.CharField(max_length=150, null=True, blank=True)
    symptoms = models.CharField(max_length=150, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return self.code
    



class ClinicProfileTwo(BaseContent):
    code = models.CharField(max_length=150, null=True, blank=True)
    detected_by_ht = models.IntegerField(null=True, blank=True)
    detected_since_ht = models.CharField(max_length=150, null=True, blank=True)
    diagnosis_ht = models.IntegerField(null=True, blank=True)
    sot_ht = models.IntegerField(null=True, blank=True)
    detected_by_dm = models.IntegerField(null=True, blank=True)
    detected_since_dm = models.CharField(max_length=150, null=True, blank=True)
    diagnosis_dm = models.IntegerField(null=True, blank=True)
    sot_dm = models.IntegerField(null=True, blank=True)
    co_morbidities = models.CharField(max_length=1000, null=True, blank=True)
    family_history = models.IntegerField(null=True, blank=True)
    tobacco = models.IntegerField(null=True, blank=True)
    alcohol = models.IntegerField(null=True, blank=True)
    smoking = models.IntegerField(null=True, blank=True)
    visit_date = models.DateField(blank=True, null=True)
    height = models.CharField(max_length=150, null=True, blank=True)
    weight = models.CharField(max_length=150, null=True, blank=True)
    bmi = models.CharField(max_length=150, null=True, blank=True)
    sbp = models.CharField(max_length=150, null=True, blank=True)
    dbp = models.CharField(max_length=150, null=True, blank=True)
    fbs = models.CharField(max_length=150, null=True, blank=True)
    ppbs = models.CharField(max_length=150, null=True, blank=True)
    rbs = models.CharField(max_length=150, null=True, blank=True)
    symptoms = models.CharField(max_length=150, null=True, blank=True)
    treatment = models.CharField(max_length=1000, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return self.code
    



class HealthProfile(BaseContent):
    code = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    detected_by_ht = models.IntegerField(null=True, blank=True)
    detected_since_ht = models.DateField(null=True, blank=True)
    diagnosis_ht = models.IntegerField(null=True, blank=True)
    sot_ht = models.IntegerField(null=True, blank=True)
    detected_by_dm = models.IntegerField(null=True, blank=True)
    detected_since_dm = models.DateField(max_length=150, null=True, blank=True)
    diagnosis_dm = models.IntegerField(null=True, blank=True)
    sot_dm = models.IntegerField(null=True, blank=True)
    is_alcoholic = models.IntegerField(default=0)
    is_tobacco = models.IntegerField(default=0)
    is_smoker = models.IntegerField(default=0)
    hyper_diabetic = models.IntegerField(default=0)
    co_morbidities = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.code

class PrescriptionProfile(BaseContent):
    code = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    medicine = models.IntegerField(blank=True, null=True)
    dosage = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.code


