from django.core.management.base import BaseCommand
from health_management.models import *
import uuid
import datetime

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
                    if cd.htn == 9:
                        ht = 2
                    elif cd.htn == 7:
                        ht = 1
                    else:
                        ht = ''
                    if cd.dm == 8:
                        dm = 2
                    elif cd.dm == 5:
                        dm = 1
                    else:
                        dm = ''
                    if cd.detected_since_dm:
                        day =cd.detected_since_dm.split('-')[0]
                        month = cd.detected_since_dm.split('-')[1]
                        year = cd.detected_since_dm.split('-')[2]
                        dm_years = datetime.date(int(year), int(month), int(day))
                    else:
                        dm_years =''
                    if cd.detected_since_htn:
                        day =cd.detected_since_htn.split('-')[0]
                        month = cd.detected_since_htn.split('-')[1]
                        year = cd.detected_since_htn.split('-')[2]
                        ht_years = datetime.date(int(year), int(month), int(day))
                    else:
                        ht_years = ''

                        

                    hts = Health.objects.create(uuid=uuid_id, user_uuid=user_uuid, 
                    patient_uuid=patient_uuid, is_alcoholic=cd.alcohol or 0, is_tobacco=cd.tobacco or 0, is_smoker=cd.smoking or 0,
                    dm_check=2,ht_check=2,dm_status=dm or 0, ht_status=ht or 0, dm_source_treatment=cd.source_treatment or 0, 
                    ht_source_treatment=cd.source_treatment  or 0,hyper_diabetic=cd.family_history or 0,
                    ht_years=ht_years or None,dm_years=dm_years or None,
                    dm_detected_by=cd.detected_by_dm or 0,ht_detected_by=cd.detected_by_htn or 0)
                    hts.save()
            except Patients.DoesNotExist:
                patients_ids = None
                        
        print('Clinic data imported is done')