from django.core.management.base import BaseCommand
from health_management.models import *
import uuid
import datetime

class Command(BaseCommand):
    help = "Patient to village profile created"

    def handle(self, *args, **options):
        health_data_two = HealthProfile.objects.filter()
        ht_date=None
        dm_date=None
        for hlt in health_data_two:
            curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
            patient_code = HealthProfile.objects.filter(code=hlt.code).first().code
            patients_ids=Patients.objects.filter( patient_id=patient_code)
            if len(patients_ids)==1:
                user_uuid = patients_ids[0].user_uuid
                patient_uuid = patients_ids[0].uuid
                if hlt.detected_since_ht:
                    ht_day = hlt.detected_since_ht.split('-')[0]
                    ht_month = hlt.detected_since_ht.split('-')[1]
                    ht_year = hlt.detected_since_ht.split('-')[2]
                    ht_date = datetime.date(int(ht_year), int(ht_month), int(ht_day))

                    
                if hlt.detected_since_dm:
                    dm_day = hlt.detected_since_dm.split('-')[0]
                    dm_month = hlt.detected_since_dm.split('-')[1]
                    dm_year = hlt.detected_since_dm.split('-')[2]
                    dm_date = datetime.date(int(dm_year), int(dm_month), int(dm_day))
                obj, created = Health.objects.update_or_create(  
                    patient_uuid=patient_uuid,
                    defaults = { 
                    "user_uuid":user_uuid,
                    "uuid":uuid_id,
                    "dm_check":2,
                    "ht_check":2,
                    "dm_status":hlt.diagnosis_dm or 0,
                    "ht_status":hlt.diagnosis_ht or 0,
                    "dm_source_treatment":hlt.sot_dm or 0, 
                    "ht_source_treatment":hlt.sot_ht  or 0,
                    "ht_years":ht_date,
                    "dm_years":dm_date, 
                    "dm_detected_by":hlt.detected_by_dm or 0,
                    "ht_detected_by":hlt.detected_by_ht or 0
                    })
                obj.server_created_on = hlt.date
                obj.save()
            elif len(patients_ids)>1:
                print('Duplicate PAteint code in system: ', patient_code)
            else:
                print('Patient ID missing: ',patient_code)
