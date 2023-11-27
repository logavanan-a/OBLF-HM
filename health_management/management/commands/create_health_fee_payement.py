from django.core.management.base import BaseCommand
from health_management.models import *
import uuid
import datetime

class Command(BaseCommand):
    help = "Patient to village profile created"

    def handle(self, *args, **options):
        # clinic_data = ClinicProfile.objects.filter(status=2)
        # patients=Patients.objects.filter(patient_id__in=clinic_data.values_list('code', flat=True))
        
        # not_imported_data = ClinicProfile.objects.exclude(code__in=patients.values_list('patient_id', flat=True))
        # for cd in clinic_data:
        #     clc_vlu = ClinicProfile.objects.filter(status=2, code=cd.code).order_by('-visit_date').first()
        #     curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        #     uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
        #     try:
        #         patients_ids=Patients.objects.get(status=2, patient_id=clc_vlu.code)
        #         user_uuid = patients_ids.user_uuid
        #         patient_uuid = patients_ids.uuid
        #         health_details = Health.objects.filter(patient_uuid=patient_uuid).exists()
        #         if user_uuid:
        #             if not health_details:
        #                 if clc_vlu.htn == 9:
        #                     ht = 2
        #                 elif clc_vlu.htn == 7:
        #                     ht = 1
        #                 else:
        #                     ht = ''
        #                 if clc_vlu.dm == 8:
        #                     dm = 2
        #                 elif clc_vlu.dm == 5:
        #                     dm = 1
        #                 else:
        #                     dm = ''
        #                 if clc_vlu.detected_since_dm:
        #                     day =clc_vlu.detected_since_dm.split('-')[0]
        #                     month = clc_vlu.detected_since_dm.split('-')[1]
        #                     year = clc_vlu.detected_since_dm.split('-')[2]
        #                     dm_years = datetime.date(int(year), int(month), int(day))
        #                 else:
        #                     dm_years =''
        #                 if clc_vlu.detected_since_htn:
        #                     day =clc_vlu.detected_since_htn.split('-')[0]
        #                     month = clc_vlu.detected_since_htn.split('-')[1]
        #                     year = clc_vlu.detected_since_htn.split('-')[2]
        #                     ht_years = datetime.date(int(year), int(month), int(day))
        #                 else:
        #                     ht_years = ''

                            

        #                 hts = Health.objects.create(uuid=uuid_id, user_uuid=user_uuid, 
        #                 patient_uuid=patient_uuid, is_alcoholic=clc_vlu.alcohol or 0, is_tobacco=clc_vlu.tobacco or 0, is_smoker=clc_vlu.smoking or 0,
        #                 dm_check=2,ht_check=2,dm_status=dm or 0, ht_status=ht or 0, dm_source_treatment=clc_vlu.source_treatment or 0, 
        #                 ht_source_treatment=clc_vlu.source_treatment  or 0,hyper_diabetic=clc_vlu.family_history or 0,
        #                 ht_years=ht_years or None,dm_years=dm_years or None,
        #                 dm_detected_by=clc_vlu.detected_by_dm or 0,ht_detected_by=clc_vlu.detected_by_htn or 0)
        #                 hts.save()
        #     except Patients.DoesNotExist:
        #         patients_ids = None
        clinic_data_two = ClinicProfileTwo.objects.filter(status=2)

        print(clinic_data_two.count(),'imported')
        patients_two=Patients.objects.filter(status=2, patient_id__in=clinic_data_two.values_list('code', flat=True))
        print(patients_two.count(),'imported')
        not_imported_data_two = ClinicProfileTwo.objects.exclude(code__in=patients_two.values_list('patient_id', flat=True))     

        print(not_imported_data_two.count(),'not imported')
        ht_date=None
        dm_date=None
        for cdw in clinic_data_two:   
            clc_vlu = ClinicProfileTwo.objects.filter(status=2, code=cdw.code).order_by('-visit_date').first()
            curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())

            patients_ids=Patients.objects.filter( patient_id=clc_vlu.code)
            if len(patients_ids)==1:
                user_uuid = patients_ids[0].user_uuid
                patient_uuid = patients_ids[0].uuid
                if clc_vlu.detected_since_ht:
                    ht_month = clc_vlu.detected_since_ht.split('-')[0]
                    ht_year = clc_vlu.detected_since_ht.split('-')[1]
                    ht_date = datetime.date(int(ht_year), int(ht_month), 1)

                    
                if clc_vlu.detected_since_dm:
                    dm_month = clc_vlu.detected_since_dm.split('-')[0]
                    dm_year = clc_vlu.detected_since_dm.split('-')[1]
                    dm_date = datetime.date(int(dm_year), int(dm_month), 1)


                obj, created = Health.objects.update_or_create(  
                patient_uuid=patient_uuid,
                defaults = { 
                "user_uuid":user_uuid,
                "uuid":uuid_id,
                "is_alcoholic":clc_vlu.alcohol or 0, 
                "is_tobacco":clc_vlu.tobacco or 0, 
                "is_smoker":clc_vlu.smoking or 0,
                "dm_check":2,
                "ht_check":2,
                "dm_status":clc_vlu.diagnosis_dm or 0,
                "ht_status":clc_vlu.diagnosis_ht or 0,
                "dm_source_treatment":clc_vlu.sot_dm or 0, 
                "ht_source_treatment":clc_vlu.sot_ht  or 0,
                "hyper_diabetic":clc_vlu.family_history or 0,
                "ht_years":ht_date,
                "dm_years":dm_date, 
                "co_morbid_names":clc_vlu.co_morbidities or None,
                "dm_detected_by":clc_vlu.detected_by_dm or 0,
                "ht_detected_by":clc_vlu.detected_by_ht or 0
                })
                obj.server_created_on = clc_vlu.visit_date
                obj.save()
            elif len(patients_ids)>1:
                print('Duplicate PAteint code in system: ', clc_vlu.code)
            else:
                print('Patient ID missing: ',clc_vlu.code)
            # else:
                # health_details = Health.objects.get(patient_uuid=patient_uuid)
                # if clc_vlu.detected_since_ht:
                #     ht_month = clc_vlu.detected_since_ht.split('-')[0]
                #     ht_year = clc_vlu.detected_since_ht.split('-')[1]
                #     ht_date = datetime.date(int(ht_year), int(ht_month), 1)

                    
                # if clc_vlu.detected_since_dm:
                #     dm_month = clc_vlu.detected_since_dm.split('-')[0]
                #     dm_year = clc_vlu.detected_since_dm.split('-')[1]
                #     dm_date = datetime.date(int(dm_year), int(dm_month), 1)
                # health_details.uuid=uuid_id 
                # health_details.user_uuid=user_uuid 
                # health_details.patient_uuid=patient_uuid
                # health_details.is_alcoholic=clc_vlu.alcohol or 0
                # health_details.is_tobacco=clc_vlu.tobacco or 0 
                # health_details.is_smoker=clc_vlu.smoking or 0
                # health_details.dm_check=2
                # health_details.ht_check=2
                # health_details.dm_status=clc_vlu.diagnosis_dm or 0 
                # health_details.ht_status=clc_vlu.diagnosis_ht or 0 
                # health_details.dm_source_treatment=clc_vlu.sot_dm or 0 
                # health_details.ht_source_treatment=clc_vlu.sot_ht  or 0
                # health_details.hyper_diabetic=clc_vlu.family_history or 0
                # health_details.ht_years=ht_date
                # health_details.dm_years=dm_date 
                # health_details.co_morbid_names = clc_vlu.co_morbidities or None
                # health_details.dm_detected_by=clc_vlu.detected_by_dm or 0
                # health_details.ht_detected_by=clc_vlu.detected_by_ht or 0
                # health_details.server_created_on = clc_vlu.visit_date
                # health_details.save()
                    