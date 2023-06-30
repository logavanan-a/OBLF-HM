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
            # print(uuid_id)
            try:
                patients_ids=Patients.objects.get(status=2, patient_id=cd.code)
                user_uuid = patients_ids.user_uuid
                patient_uuid = patients_ids.uuid
                health_details = Health.objects.filter(patient_uuid=patient_uuid).exists()
                if not health_details:
                    Health.objects.create(uuid=uuid_id, user_uuid=user_uuid, 
                    patient_uuid=patient_uuid, is_alcoholic=cd.alcohol, is_tobacco=cd.tobacco, is_smoker=cd.smoking,
                    dm_check=2,ht_check=2,dm_status=, ht_status=,dm_source_treatment=,ht_source_treatment=,
                    dm_years=cd.detected_since_dm,ht_years=cd.detected_since_htn,dm_detected_by=,ht_detected_by=)
            except Patients.DoesNotExist:
                patients_ids = None
                print(';;;;')
                        
        print('Clinic data imported is done')