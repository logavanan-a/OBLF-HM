from django.core.management.base import BaseCommand
from health_management.models import *
import uuid

class Command(BaseCommand):
    help = "Patient to village profile created"

    def handle(self, *args, **options):
        clinic_data = ClinicProfile.objects.filter(status=2)
        print(clinic_data.count(), 'clinic_count')
        patients=Patients.objects.filter(patient_id__in=clinic_data.values_list('code', flat=True))
        print(patients.count(), 'patient_count')
        not_imported_data = ClinicProfile.objects.exclude(code__in=patients.values_list('patient_id', flat=True))
        print(not_imported_data.count(),'not')
        
        for cd in clinic_data:
            curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
            print(uuid_id)
            try:
                patients_ids=Patients.objects.get(status=2, patient_id=cd.code)
                user_uuid = patients_ids.user_uuid
                patient_uuid = patients_ids.uuid
                treatment_details = Treatments.objects.filter(patient_uuid=patient_uuid, visit_date__date=cd.visit_date).exists()
                if not treatment_details:
                    treatment_obj = Treatments.objects.create(uuid=uuid_id,
                    user_uuid=user_uuid, patient_uuid=patient_uuid, 
                    visit_date=cd.visit_date, bp_sys1=cd.sbp, bp_non_sys1=cd.dbp,
                    fbs=cd.fbs, pp=cd.ppbs, random=cd.rbs, symptoms=cd.symptoms,
                    remarks=cd.remarks, bmi=cd.bmi, weight=cd.weight, 
                    hyper_diabetic=cd.family_history, is_tobacco=cd.tobacco, 
                    is_alcoholic=cd.alcohol, is_smoker=cd.smoking)
                    treatment_obj.save()
                # diagnosis_details_tn = Diagnosis.objects.filter(patient_uuid=patient_uuid, ndc_id=cd.htn).exists()
                # if not diagnosis_details_tn:
                #     print('TN')
                # diagnosis_details_dm = Diagnosis.objects.filter(patient_uuid=patient_uuid, ndc_id=cd.dm).exists()
                # if not diagnosis_details_dm:
                #     print('DM')


            except Patients.DoesNotExist:
                patients_ids = None
                
            


        
        print('Clinic data imported is done')