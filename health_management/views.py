from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from application_masters.models import *
from .serializer import *
from django.http import JsonResponse
from rest_framework.response import Response

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
            #Village Site
            village_sites=Village.objects.filter(phc=valid_user.phc)
            if data.get('village_sites_smo_date'):
                village_sites= village_sites.filter(server_modified_on__gt = data.get('village_sites_smo_date'))
            villagesites_serializer=VillageSerializers(village_sites,many=True)
            #Medicines
            medicines=Medicines.objects.filter(status=2)
            if data.get('medicine_smo_date'):
                medicines= medicines.filter(server_modified_on__gt = data.get('medicine_smo_date'))
            medicineserializer=MedicineSerializers(medicines,many=True)

            #userdata
            userprofileserializer=UserProfileSerializers(valid_user)

            #patient data
            village_sites_ids=village_sites.values_list('id',flat=True)
            patient_smo_date = Patients.objects.filter(status=2,mhu_site_id__in=village_sites_ids).order_by('server_modified_on')
            patient_uuids=patient_smo_date.values_list('uuid',flat=True)
            if data.get('patient_smo_date'):
                patient_smo_date= patient_smo_date.filter(server_modified_on__gt = data.get('patient_smo_date'))
            patientSerializers = PatientSerializers(patient_smo_date,many=True)
            
            #patient treatment 
            patient_treatment_smo_date = Treatments.objects.filter(status=2,patient_uuid__in=patient_uuids).order_by('server_modified_on')
            patient_treatment_uuds=patient_treatment_smo_date.values_list('uuid',flat=True)
            if data.get('patient_treatment_smo_date'):
                patient_treatment_smo_date= patient_treatment_smo_date.filter(server_modified_on__gt = data.get('patient_treatment_smo_date'))
            patient_treatmentSerializers = TreatmentSerializers(patient_treatment_smo_date,many=True)

            
            #medicine
            medicine_dis_smo_date = Prescription.objects.filter(status=2,visit_uuid__in=patient_visit_uuds).order_by('server_modified_on')
            if data.get('medicine_dis_smo_date'):
                medicine_dis_smo_date= medicine_dis_smo_date.filter(server_modified_on__gt = data.get('medicine_dis_smo_date'))
            prescriptionSerializers = PrescriptionSerializers(medicine_dis_smo_date,many=True)
            
            jsonresponse_full = {
                "status":2,
                "message":"Data Already Sent",
            } 
            jsonresponse_full['village_sites'] = mhusite_serializer.data
            jsonresponse_full['medicines'] = medicineserializer.data
            jsonresponse_full['user_data'] = userprofileserializer.data
            jsonresponse_full['patient'] = patientSerializers.data
            jsonresponse_full['prescription'] = prescriptionSerializers.data
            jsonresponse_full['visit'] = patient_treatmentSerializers.data

            return Response(jsonresponse_full)
        else:
            return Response({
            "status":0,
            "message":"Phc does not exits"
            })


            

