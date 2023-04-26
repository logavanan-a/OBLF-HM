from django.core.management.base import BaseCommand
from health_management.models import *
import uuid



class Command(BaseCommand):
    help = "Patient to village profile created"

    def handle(self, *args, **options):
        village_data = VillageProfile.objects.filter(status=2)
        curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        uuid_id = str(curr_dt) + "-" + str(uuid.uuid4())
        for vd in village_data:
            patients=Patients.objects.filter(patient_id=vd.patient_id).exists()
            if not patients:
                vg=VillageProfile.objects.filter(patient_id=vd.patient_id)
                vg.update(data_migration=3)
                user_id=UserProfile.objects.filter(village=vd.village).first()
                patients_obj=Patients.objects.create(patient_id=vd.patient_id,
                uuid=user_id.uuid,user_uuid=uuid_id,name=vd.name,dob=vd.dob,
                age=vd.age,village=vd.village,phone_number=vd.phone_number,
                image=vd.image,gender=vd.gender,subcenter_id=vd.subcenter_id,door_no=vd.door_no,
                seq_no=vd.seq_no)
                patients_obj.save()
            elif patients:
                vg=VillageProfile.objects.filter(patient_id=vd.patient_id)
                vg.update(data_migration=2)
           