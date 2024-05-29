from django.core.management.base import BaseCommand
from health_management.models import *
import uuid



class Command(BaseCommand):
    help = "Patient to village profile created"

    def handle(self, *args, **options):
        prescription_data_two = PrescriptionProfile.objects.filter()
        for prp in prescription_data_two:
            curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
            patient_code = PrescriptionProfile.objects.filter(code=prp.code).first().code
            patients_ids=Patients.objects.filter(patient_id=patient_code)
            if len(patients_ids)==1:
                user_uuid = patients_ids[0].user_uuid
                patient_uuid = patients_ids[0].uuid
                trmt_vlu = Treatments.objects.filter(patient_uuid=patient_uuid, visit_date__date=prp.date)
                # import ipdb;ipdb.set_trace()
                mds = Medicines.objects.filter(id=prp.medicine)
                if len(trmt_vlu) == 1 and len(trmt_vlu) != 0:
                    if not Prescription.objects.filter(treatment_uuid=trmt_vlu[0].uuid, patient_uuid=trmt_vlu[0].patient_uuid, server_created_on__date=prp.date, medicines_id=mds[0].id).exists():
                        prp_obj = Prescription.objects.create(  
                                treatment_uuid=trmt_vlu[0].uuid,
                                patient_uuid=trmt_vlu[0].patient_uuid,
                                user_uuid=trmt_vlu[0].user_uuid,
                                uuid=uuid_id,
                                medicines_id=mds[0].id,
                                dosage_id=prp.dosage or None,
                                medicine_type=mds[0].medicines_type or None,
                                qty=prp.qty or None,
                            )
                        prp_obj.save()
                        prp_obj.server_created_on = prp.date
                        prp_obj.save()
                        prp.status=2
                elif len(trmt_vlu)>1:
                    print('Duplicate Treatment code in system: ', patient_code,':',prp.date)
                    prp.status=1
                else:
                    prp.status=1
                    print('Treatments ID missing: ',patient_code,':',prp.date)
            elif len(patients_ids)>1:
                prp.status=1
                print('Duplicate Pateint code in system: ', patient_code)
            else:
                prp.status=1
                print('Patient ID missing: ',patient_code)
            prp.save()

