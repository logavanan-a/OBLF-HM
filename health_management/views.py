from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import transaction
from django.http import HttpResponseRedirect
from application_masters.models import *
from .serializer import *
from django.http import JsonResponse
from rest_framework.response import Response
import json
import sys, os

# Create your views here.


def login_view(request):
    heading = "Login"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            findUser = User._default_manager.get(username__iexact=username)
        except User.DoesNotExist:
            findUser = None
        if findUser is not None:
            username = findUser.get_username()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home_view/')
        else:
            logout(request)
            error_message = "Invalid Username and Password"
    return render(request, 'dashboard/login.html', locals())



@ login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def home_view(request):
     return render(request, 'learning/sql_listing.html', locals())



class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        user = None
        username = data.get('username')
        password = data.get('password')
        try:
            findUser = UserProfile._default_manager.get(
                user__username__iexact=username)            
        except UserProfile.DoesNotExist:
            findUser = None
        if findUser is not None:
            username = findUser.user.get_username()
            user = authenticate(request, username=username, password=password)
        if user is not None:
            userprofileserialize=UserProfileSerializers(findUser)
            return JsonResponse({
                "uId": user.id,
                "message": "Logged in successfully",
                "status": 2,
                "userprofile":[userprofileserialize.data]
            })
        else:
            return JsonResponse({
                "message": "Invalid username or password",
                "status": 0,
            })

class Phc_pull(APIView):
    permission_classes = ()
    def post(self, request, pk):
        data = request.build_absolute_uri()
        data= request.data
        try:
            valid_user = UserProfile.objects.get(uuid = pk)
        except:
            return Response({"message":"Invalid UUID"})

        if valid_user:
            #Village
            villages=valid_user.village
            villagesites_serializer=VillageSerializers(villages)

            #State
            stateserializer=StateSerializers(valid_user.village.subcenter.phc.taluk.district.state)
            #district
            districtserializers=DistrictSerializers(valid_user.village.subcenter.phc.taluk.district)
            #taluk
            talukserializers=TalukSerializers(valid_user.village.subcenter.phc.taluk)
            #phc
            phcserializers=PHCSerializers(valid_user.village.subcenter.phc)

            #subcenter
            subcenterserializers=SubcenterSerializers(valid_user.village.subcenter)

            #ndcs
            ndcs=MasterLookup.objects.filter(parent__id=4)
            ndcserializers=MasterLookupSerializers(ndcs,many=True)

            #Medicines
            medicines=Medicines.objects.filter(status=2)
            medicineserializer=MedicineSerializers(medicines,many=True)

            #comorbids
            comorbids = Comorbid.objects.filter(status=2)
            comorbidserializers=ComorbidSerializers(comorbids,many=True)

            #dosage
            dosage=Dosage.objects.filter(status=2)
            dosageserializer=DosageSerializers(dosage,many=True)

            #userdata
            userprofileserializer=UserProfileSerializers(valid_user)

            # patient data
            patient_visit_type=MasterLookup.objects.filter(parent__id=6)
            patient_smo_date = Patients.objects.filter(status=2, patient_visit_type__in=patient_visit_type).order_by('server_modified_on')
            patient_uuids=patient_smo_date.values_list('uuid',flat=True)
            if data.get('patient_smo_date'):
                patient_smo_date= patient_smo_date.filter(server_modified_on__gt = data.get('patient_smo_date'))
            patientSerializers = PatientSerializers(patient_smo_date,many=True)
            
            # patient treatment 
            patient_treatment_smo_date = Treatments.objects.filter(status=2,patient_uuid__in=patient_uuids).order_by('server_modified_on')
            patient_treatment_uuids=patient_treatment_smo_date.values_list('uuid',flat=True)
            if data.get('treatment_smo_date'):
                patient_treatment_smo_date= patient_treatment_smo_date.filter(server_modified_on__gt = data.get('treatment_smo_date'))
            patient_treatmentSerializers = TreatmentSerializers(patient_treatment_smo_date,many=True)

            
            # medicine
            prescription_smo_date = Prescription.objects.filter(status=2).order_by('server_modified_on')
            if data.get('prescription_smo_date'):
                prescription_smo_date = prescription_smo_date.filter(server_modified_on__gt = data.get('prescription_smo_date'))
            prescriptionserializers = PrescriptionSerializers(prescription_smo_date,many=True)

            #diagnosis
            ndcs=MasterLookup.objects.filter(parent__id=4)
            diagnosis_smo_date = Diagnosis.objects.filter(status=2, ndc__in=ndcs).order_by('server_modified_on')
            if data.get('diagnosis_smo_date'):
                diagnosis_smo_date = diagnosis_smo_date.filter(server_modified_on__gt = data.get('diagnosis_smo_date'))
            diagnosisserializers = DiagnosisSerializers(diagnosis_smo_date,many=True)

            
            scanned_report_smo_date = Scanned_Report.objects.filter(status=2).order_by('server_modified_on')
            if data.get('scanned_report_smo_date'):
                scanned_report_smo_date = scanned_report_smo_date.filter(server_modified_on__gt = data.get('scanned_report_smo_date'))
            scanned_reportserializers = ScannedReportSerializers(scanned_report_smo_date,many=True)

            jsonresponse_full = {
                "status":2,
                "message":"Data Already Sent",
            } 
            jsonresponse_full['villages'] = [villagesites_serializer.data]
            jsonresponse_full['state'] = [stateserializer.data]
            jsonresponse_full['district'] = [districtserializers.data]
            jsonresponse_full['taluk'] = [talukserializers.data]
            jsonresponse_full['phc'] = [phcserializers.data]
            jsonresponse_full['subcenter'] = [subcenterserializers.data]
            jsonresponse_full['medicines'] = medicineserializer.data
            jsonresponse_full['dosage'] = dosageserializer.data
            jsonresponse_full['ndcs'] = ndcserializers.data
            jsonresponse_full['comorbids'] = comorbidserializers.data
            jsonresponse_full['user_data'] = userprofileserializer.data

            jsonresponse_full['patients'] = patientSerializers.data
            jsonresponse_full['treatment'] = patient_treatmentSerializers.data
            jsonresponse_full['prescription'] = prescriptionserializers.data
            jsonresponse_full['diagnosis'] = diagnosisserializers.data
            jsonresponse_full['scanned_report'] = scanned_reportserializers.data

            return Response(jsonresponse_full)
        else:
            return Response({
            "status":0,
            "message":"Phc does not exits"
            })


class Phc_push(APIView):
    def post(self,request,pk):
        patient_success =[]
        diagnosis_success =[]
        prescription_success =[]
        treatment_success =[]
        scanned_report_success =[]
        try:
            data = request.build_absolute_uri()
            data = request.data
            # import ipdb
            # ipdb.set_trace()
            patient_response = {'data':[]}
            diagnosis_response = {'data':[]}
            prescription_response = {'data':[]}
            treatment_response = {'data':[]}
            scanned_report_response = {'data':[]}

            try:
                valid_user = UserProfile.objects.filter(uuid = pk)
            except:
                return Response({"message":"Invalid UUID"})
            #-TODO-valid user based on that mhu
            if  valid_user :
                user = valid_user.first()
                with transaction.atomic():
                    user_data = data.get('userdata')
                    patient_data  = patient_details(request)
                    for obj in patient_data:
                        patient_info ={}
                        patient_info['uuid']=obj.uuid
                        patient_info['patient_id'] = obj.patient_id
                        patient_info['SCO'] = obj.server_created_on
                        patient_info['SMO'] = obj.server_modified_on
                        patient_info['sync_status'] = obj.sync_status
                        patient_response['data'].append(patient_info)
                        patient_success =  patient_response['data']

                    
                    diagnosis_data  = diagnosis_details(data)
                    for obj in diagnosis_data:
                        diagnosis_info ={}
                        diagnosis_info['uuid']=obj.uuid
                        diagnosis_info['SCO'] = obj.server_created_on
                        diagnosis_info['SMO'] = obj.server_modified_on
                        diagnosis_info['sync_status'] = obj.sync_status
                        diagnosis_response['data'].append(diagnosis_info)
                        diagnosis_success =  diagnosis_response['data']
    
                    
                    prescription_data  = prescription_details(data)
                    for obj in prescription_data:
                        prescription_info ={}
                        prescription_info['uuid']=obj.uuid
                        prescription_info['SCO'] = obj.server_created_on
                        prescription_info['SMO'] = obj.server_modified_on
                        prescription_info['sync_status'] = obj.sync_status
                        prescription_response['data'].append(prescription_info)
                        prescription_success =  prescription_response['data']
    
                    treatment_data  = treatment_details(data)
                    for obj in treatment_data:
                        treatment_info ={}
                        treatment_info['uuid']=obj.uuid
                        treatment_info['SCO'] = obj.server_created_on
                        treatment_info['SMO'] = obj.server_modified_on
                        treatment_info['sync_status'] = obj.sync_status
                        treatment_response['data'].append(treatment_info)
                        treatment_success =  treatment_response['data']

                    
                    scanned_report_data  = scanned_report_details(data)
                    for obj in scanned_report_data:
                        scanned_report_info ={}
                        scanned_report_info['uuid']=obj.uuid
                        scanned_report_info['SCO'] = obj.server_created_on
                        scanned_report_info['SMO'] = obj.server_modified_on
                        scanned_report_info['sync_status'] = obj.sync_status
                        scanned_report_response['data'].append(scanned_report_info)
                        scanned_report_success =  scanned_report_response['data']
    


            else :
                return Response({
                "message":"User does not exits"
                })
                
            return Response({
                "status":2,
                "message":"Data Already Sent",
                "patient_data" : patient_success,
                "diagnosis_data" : diagnosis_success,
                "prescription_data" : prescription_success,
                "treatment_data" : treatment_success,
                "scanned_report_data" : scanned_report_success,
            })

        except Exception as e:
            return Response({
                "status":0,
                "message":str(e),
                "patient_data" : patient_success,
                "diagnosis_data" : diagnosis_success,
                "prescription_data" : prescription_success,
                "treatment_data" : treatment_success,
                "scanned_report_data" : scanned_report_success,
            })
    
def patient_details(self):
    objlist =[]
    # import ipdb
    # ipdb.set_trace()
    for data in json.loads(self.data.get('patients')):
        obj, created = Patients.objects.update_or_create(
            uuid = data.get('uuid'),
            defaults= {
                        "name" : data.get('name'),
                        "dob" : data.get('dob'),
                        "age":data.get('age'),
                        "gender" : data.get('gender'),
                        "village_id" : data.get('village_id'),
                        # "village__phc_id" : data.get('phc_id'),
                        # "state_id" : data.get('state_id'),
                        # "district_id" : data.get('district_id'),
                        # "taluk_id" : data.get('taluk_id'),
                        "phone_number": data.get('phone'),
                        "image": self.FILES.get(data.get('uuid')),
                        "height":data.get('height'),
                        "weight":data.get('weight'),
                        "door_no":data.get('door_no'),
                        "seq_no":data.get('seq_no'),
                        "patient_visit_type_id": data.get('patient_visit_type'),                        
                        "fee_status":data.get('fee_status'),
                        "fee_paid":data.get('fee_paid'),
                        "fee_date":data.get('fee_date'),
                        "registered_date":data.get('registered_date'),
                        "last_visit_date":data.get('last_visit_date'),
                        })
        if created:
            obj.patient_id = data.get('patient_id')+'-'+str('%05d' % obj.id)

        obj.save()
        
        objlist.append(obj)

    return objlist


def treatment_details(self):
    objlist = []

    for data in json.loads(self.get('treatment')):
        obj,created = Treatments.objects.update_or_create(
            uuid = data.get('uuid'),
            patient_uuid = data.get('patient_uuid'),

            defaults = {
                    "visit_date" : data.get('visit_date'),
                    "bp_sys1" : data.get('bp_sys1'),
                    "bp_non_sys1" : data.get('bp_non_sys1'),
                    "bp_sys2" : data.get('bp_sys2'),
                    "bp_non_sys2" : data.get('bp_non_sys2'),
                    "bp_sys3" : data.get('bp_sys3'),
                    "bp_non_sys3" : data.get('bp_non_sys3'),
                    "fbs" : data.get('fbs'),
                    "pp" : data.get('pp'),
                    "random" : data.get('random'),
                    "weight" : data.get('weight'),
                    # "height" : data.get('height'),
                    "bmi" : data.get('bmi'),
                    "symptoms" : data.get('symptoms'),
                    "remarks" : data.get('remarks'),
                    "co_morbid_ids" : data.get('co_morbid_ids'),
                    "co_morbid_names" : data.get('co_morbid_names'),
                    "hyper_diabetic" : data.get('hyper_diabetic'),
                    "is_alcoholic" : data.get('is_alcoholic'),
                    # "sub_category_names" : data.get('sub_category_names'),
                    "is_tobacco":data.get('is_tobacco'),
                    "is_smoker":data.get('is_smoker'),
                    })
        objlist.append(obj)

    return objlist


def prescription_details(self):
    objlist = []
    for data in json.loads(self.get('prescription')):
        obj,created = Prescription.objects.update_or_create(
            uuid = data.get('uuid'),
            patient_uuid = data.get('patient_uuid'),

            defaults = {
                    "treatment_uuid" : data.get('treatment_uuid'),
                    "medicines_id" : data.get('medicine_id'),
                    "dosage_id" : data.get('dosage'),
                    "no_of_days" : data.get('no_of_days'),
                    "medicine_type" : data.get('medicine_type'),
                    "qty" : data.get('qty'),
                    })
        objlist.append(obj)

    return objlist



def diagnosis_details(self):
    objlist = []
    for data in json.loads(self.get('diagnosis')):
        obj,created = Diagnosis.objects.update_or_create(
            uuid = data.get('uuid'),

            defaults = {
                    "treatment_uuid" : data.get('treatment_uuid'),
                    "source_treatment" : data.get('source_treatment'),
                    "ndc_id" : data.get('ndc_id'),
                    "source_treatment" : data.get('source_treatment'),
                    "years" : data.get('years'),
                    "detected_by" : data.get('detected_by'),
                    })
        objlist.append(obj)

    return objlist


def scanned_report_details(self):
    objlist = []
    for data in json.loads(self.get('scanned_report')):
        obj,created = Scanned_Report.objects.update_or_create(
            uuid = data.get('uuid'),
            patient_uuid = data.get('patient_uuid'),

            defaults = {
                    "title" : data.get('title'),
                    "image_path" : data.get('image_path'),
                    "captured_date" : data.get('captured_date'),
                    })
        objlist.append(obj)

    return objlist



        


  


  
