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
        print(clinic_data.count() - patients.count(), 'total pending data')
        not_imported_data = ClinicProfile.objects.exclude(code__in=patients.values_list('patient_id', flat=True))
        print(not_imported_data.count())
        curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
        for cd in clinic_data:
            patients=Patients.objects.filter(patient_id=cd.code)
            print(patients.count())

        
        print('Clinic data imported is done')