from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from application_masters.models import *
from health_management.models import *
from .serializer import *
from .forms import *
from django.http import JsonResponse
from rest_framework.response import Response
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import sys, os
from datetime import datetime
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import localtime
import csv





# Create your views here.


def pagination_function(request, data):
    records_per_page = 10
    paginator = Paginator(data, records_per_page)
    page = request.GET.get('page', 1)
    try: 
        pagination = paginator.page(page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)
    return pagination

def login_view(request):
    heading = "Login"
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/list/userprofile/')
        else:
            logout(request)
            error_message = "Invalid Username and Password"
    return render(request, 'dashboard/login.html', locals())



@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def drug_prescription_csv_export(request):
    response = HttpResponse(content_type='text/csv',)
    response['Content-Disposition'] = 'attachment; filename="Drug prescription'+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'PHC Name',
        'Sub Centre',
        'Village',
        'Patient Name',
        'Medicine', 
        'Quantity', 
        'Visit Date', 
        'Created On', 
        ])
    prescription_csv = Prescription.objects.filter()
    for prescription in prescription_csv:
        patient = prescription.get_user_uuid()
        treatment = prescription.get_treatment_uuid()
        writer.writerow([
            patient.village.subcenter.phc if patient else '',
            patient.village.subcenter if patient else '',
            patient.village if patient else '',
            patient.name if patient else '',
            prescription.medicines,
            prescription.qty,
            treatment.visit_date.strftime("%m/%d/%Y %I:%M %p") if treatment else '', 
            prescription.server_created_on.strftime("%m/%d/%Y %I:%M %p"),
             ])
    return response

    

def distribution_village_wise_csv(request):
    response = HttpResponse(content_type='text/csv',)
    response['Content-Disposition'] = 'attachment; filename="distribution village wise medicine'+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'PHC Name',
        'Sub Centre',
        'Village', 
        'Medicine',
        'Quantity'
        ])
    distribution_csv = Prescription.objects.filter()
    for distribution in distribution_csv:
        patient = distribution.get_user_uuid()
        qty = distribution.get_qty()
        writer.writerow([
            patient.village.subcenter.phc if patient else '',
            patient.village.subcenter if patient else '',
            patient.village if patient else '',
            distribution.medicines,
            qty
            ])
    return response 


def verified_diagnosis_report(request):
    heading="VERFIED DIAGNOSIS"
    verified_diagnosis_list = Diagnosis.objects.filter(status=2)
    filter_values = request.GET.dict()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="verified diagnosis'+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village',                                   
            'Patient Name',
            'Patient Code',
            'NCD',
            'Source of treatment',
            'Health Worker'
            ])
        for diagnosis in verified_diagnosis_list:
            patient = diagnosis.get_patients_uuid()
            health_worker = diagnosis.get_health_worker()
            writer.writerow([
                patient.village.subcenter.phc if patient else '',
                patient.village.subcenter if patient else '',
                patient.village if patient else '',
                patient.name if patient else '',
                patient.patient_id if patient else '',
                diagnosis.ndc,
                diagnosis.source_treatment,
                health_worker.user.first_name if health_worker else ''
                ])
        return response 
    return render(request, 'reports/verified_diagnosis.html', locals())

def verified_home_visit_report(request):
    heading="VERFIED HEALTH WORKERS HOME VISITS"
    verified_home_visit = HomeVisit.objects.filter(status=2)
    filter_values = request.GET.dict()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="verified home visit '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village',                                   
            'Patient Name',
            'Patient Code',
            'Home visit',
            'Last date of visit',
            'Health Worker'
            ])
        for home_visit in verified_home_visit:
            patient = home_visit.get_patient_uuid()
            health_worker = home_visit.get_health_worker()
            writer.writerow([
                patient.village.subcenter.phc if patient else '',
                patient.village.subcenter if patient else '',
                patient.village if patient else '',
                patient.name if patient else '',
                patient.patient_id if patient else '',
                home_visit.get_home_vist_display(),
                home_visit.response_datetime,
                health_worker.user.first_name if health_worker else ''
                ])
        return response 
    return render(request, 'reports/verified_home_visit.html', locals())




def verified_treatments_report(request):
    heading="VERFIED TREATMENTS"
    verified_treatments = Treatments.objects.filter(status=2)
    filter_values = request.GET.dict()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="verified treatment '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village',                                   
            'Patient Name',
            'Patient Code',
            'DOB',
            'Age(today)',
            'Gender',
            'SBP1',
            'SBP2',
            'SBP3',
            'DBP1',
            'DBP2',
            'DBP3',
            'Blood Sugar Fasting',
            'Blood Sugar PP',
            'Blood Sugar Random',
            'Visit Date',
            ])
        for treatments in verified_treatments:
            patient = treatments.get_patients_uuid()
            writer.writerow([
                patient.village.subcenter.phc if patient else '',
                patient.village.subcenter if patient else '',
                patient.village if patient else '',
                patient.name if patient else '',
                patient.patient_id if patient else '',
                patient.dob if patient else '',
                patient.calculate_age() if patient else '',
                patient.get_gender_display() if patient else '',
                treatments.bp_sys1,
                treatments.bp_sys2,
                treatments.bp_sys3,
                treatments.bp_non_sys1,
                treatments.bp_non_sys2,
                treatments.bp_non_sys3,
                treatments.fbs,
                treatments.pp,
                treatments.random,
                treatments.visit_date.strftime("%m/%d/%Y %I:%M %p"),
                ])
        return response
    return render(request, 'reports/verified_treatments.html', locals())


def home_visit_report(request):
    heading="HEALTH WORKERS HOME VISITS"
    filter_values = request.GET.dict()
    from dateutil.relativedelta import relativedelta
    health_worker_obj = UserProfile.objects.filter(status=2)
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '0')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    health_worker = request.GET.get('health_worker', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    health_worker_ids = int(health_worker) if health_worker != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    health_worker_in_patient = True
    s_date=''
    e_date=''
    between_date = ""
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
        between_date = """and to_char(hv.response_datetime,'YYYY-MM-DD') >= '"""+s_date + \
            """' and to_char(hv.response_datetime,'YYYY-MM-DD') <= '""" + \
            e_date+"""' """
    phc_id=""
    if phc_ids:
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        get_phc_name = PHC.objects.get(id=phc_ids)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center_ids:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        sbc_ids = '''and sbc.id='''+sub_center
    village_id=""
    if village_ids:
        get_village_name = Village.objects.get(id=village_ids)
        village_id = '''and vlg.id='''+village
    hwk_id=""
    if health_worker_ids:
        get_health_worker_name = User.objects.get(id=health_worker_ids)
        hwk_id = '''and upf.user_id='''+health_worker
    cursor = connection.cursor()
    cursor.execute('''select phc.name as phc_name, sbc.name as sbc_name, vlg.name as village_name, pt.name as patient_name, pt.patient_id as patient_code, 
    count(pt.patient_id) as no_of_visits, max(hv.response_datetime) as last_date_of_visit, hwn.first_name as health_worker_name from health_management_homevisit hv 
    inner join health_management_patients pt on hv.patient_uuid = pt.uuid inner join application_masters_village vlg on pt.village_id=vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id inner join application_masters_phc phc on sbc.phc_id = phc.id 
    inner join health_management_userprofile upf on hv.user_uuid=upf.uuid inner join auth_user hwn on upf.user_id = hwn.id
    where 1=1 '''+phc_id+sbc_ids+village_id+hwk_id+between_date+''' group by phc_name, sbc_name, village_name, patient_name, patient_code, health_worker_name order by vlg.name''')
    home_visit_data = cursor.fetchall()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="Health worker home visit '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['HEALTH WORKER HOME VISIT'])
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village', 
            'Patient Name',
            'Patient Code',
            'Number of visit',
            'Last date of visit',
            'Health Worker'
            ])
        for data in data:
            writer.writerow([
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7]
            ])
        return response
    data = pagination_function(request, home_visit_data)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/home_visit.html', locals())


def clinic_level_statistics_list(request):
    heading="CLINIC LEVEL STATISTICS"
    filter_values = request.GET.dict()
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    s_date=''
    e_date=''
    between_date = ""
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
        between_date = """and to_char(pt.server_created_on,'YYYY-MM-DD') >= '"""+s_date + \
            """' and to_char(pt.server_created_on,'YYYY-MM-DD') <= '""" + \
            e_date+"""' """
    phc_id= ""
    if phc:
        get_phc_name = PHC.objects.get(id=phc_ids)
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        sbc_ids = '''and sbc.id='''+sub_center
    village_id=""
    if village:
        get_village_name = Village.objects.get(id=village_ids)
        village_id = '''and vlg.id='''+village
    
    cursor = connection.cursor()
    cursor.execute('''select phc.name as phc_name, sbc.name as sbc_name , vlg.name as vlg_name, 
    date(trmt.visit_date) as date_of_clinic, count(trmt.uuid) as total, coalesce(sum(case when trmt.visit_date=pt.registered_date then 1 else 0 end),0) as rg_date 
    from  health_management_treatments trmt left join health_management_patients as pt on trmt.patient_uuid=pt.uuid 
    inner join application_masters_village vlg on pt.village_id = vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id 
    inner join application_masters_phc phc on sbc.phc_id = phc.id 
    where 1=1 '''+phc_id+sbc_ids+village_id+between_date+''' 
    group by phc.name, sbc.name, vlg.name, date(trmt.visit_date)
    order by vlg.name''')

    clinic_level_data = cursor.fetchall()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="clinic level statistics'+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['CLININ LEVEL STATISTICS'])
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village', 
            'Dates of clinics',
            'New registration',
            'Total no of consultations'
            ])
        for data in data:
            writer.writerow([
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
            ])
        return response
    data = pagination_function(request, clinic_level_data)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/clinic_level_statistics.html', locals())

def village_wise_drugs_list(request):
    heading="village wise drug dispensation"
    search = request.GET.get('search', '')
    if search:
        drug_dispensation = DrugDispensation.objects.filter(Q(Q(medicine__name__icontains=search)|Q(village__name__icontains=search)), status=2)
    else:
        drug_dispensation = DrugDispensation.objects.filter(status=2)
    data = pagination_function(request, drug_dispensation)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'manage_stocks/village_wise_drug_dispensation/village_wise_drug_list.html', locals())

def add_village_wise_drugs(request):
    heading="Add the village wise drug dispensation"
    now = datetime.now()
    current_data = now.strftime("%Y-%m-%d")
    medicine_search = request.GET.get('medicine_search', '')
    village_search = request.GET.get('village_search', '')
    if medicine_search:
        medicine = Medicines.objects.filter(name__icontains=medicine_search)
    else:
        medicine = Medicines.objects.filter(status=2)
    if village_search:
        village = Village.objects.filter(name__icontains=village_search)
    else:
        village = Village.objects.filter(status=2)
    if request.method == 'POST':
        data = request.POST
        for mids in medicine:
            for vids in village:
                if data.get(str(mids.id)+'_units_dispensed_'+str(vids.id)):
                    units_dispensed = data.get(str(mids.id)+'_units_dispensed_'+str(vids.id))
                    date_of_dispensation = data.get('date_of_dispensation')
                    drug_dispensation = DrugDispensation.objects.create(medicine=mids, village=vids,
                     units_dispensed=units_dispensed, date_of_dispensation=date_of_dispensation)    
                    drug_dispensation.save()
        return redirect('/village-wise-drugs/list/')
    return render(request, 'manage_stocks/village_wise_drug_dispensation/add_village_wise_drugs.html', locals())

def drug_dispensation_stock_list(request):
    heading="Drugs Dispensation reports"
    filter_values = request.GET.dict()
    medicine_obj=Medicines.objects.filter(status=2)
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    medicine = request.GET.get('medicine', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    medicine_ids = int(medicine) if medicine != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    s_date=''
    e_date=''
    medicine_list = True
    prescription_list=Prescription.objects.filter(status=2)
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
        prescription_list=prescription_list.filter(status=2, server_created_on__range=[s_date,e_date])
    if phc_ids:
        get_phc_name = PHC.objects.get(id=phc_ids)
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        pateint_registration_report = Patients.objects.filter(village__subcenter__phc__id=phc_ids).values_list('uuid')
        prescription_list = prescription_list.filter(patient_uuid__in=pateint_registration_report)
    if sub_center_ids:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        pateint_registration_report = Patients.objects.filter(village__subcenter__id=sub_center_ids).values_list('uuid')
        prescription_list = prescription_list.filter(patient_uuid__in=pateint_registration_report)
    if village_ids:
        get_village_name = Village.objects.get(id=village_ids)
        pateint_registration_report = Patients.objects.filter(village__id=village_ids).values_list('uuid')
        prescription_list = prescription_list.filter(patient_uuid__in=pateint_registration_report)
    if medicine_ids:
        get_medicine_name = Medicines.objects.get(id=medicine_ids)
        prescription_list = prescription_list.filter(medicines__id=medicine_ids)
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="Drug prescription'+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['DRUG PRESCRIPTION'])
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village',
            'Patient Name',
            'Patient Code',
            'Medicine', 
            'Quantity', 
            'Visit Date', 
            'Created On', 
            ])
        for prescription in prescription_list:
            patient = prescription.get_user_uuid()
            treatment = prescription.get_treatment_uuid()
            writer.writerow([
                patient.village.subcenter.phc if patient else '',
                patient.village.subcenter if patient else '',
                patient.village if patient else '',
                patient.name if patient else '',
                patient.patient_id if patient else '',
                prescription.medicines,
                prescription.qty,
                treatment.visit_date.strftime("%m/%d/%Y %I:%M %p") if treatment else '', 
                prescription.server_created_on.strftime("%m/%d/%Y %I:%M %p"),
                ])
        return response

    data = pagination_function(request, prescription_list)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/drug_dispensation_list.html', locals())

def medicine_stock_list(request):
    heading="Medicine stocks detatials"
    search = request.GET.get('search', '')
    if search:
        medicine_stock = MedicineStock.objects.filter(medicine__name__icontains=search)
    else:
        medicine_stock = MedicineStock.objects.filter(status=2)
    data = pagination_function(request, medicine_stock)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'manage_stocks/medicine_stock/medicine_list.html', locals())

def patient_registration_report(request):
    heading="Patient Registration Report"
    filter_values = request.GET.dict()
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    s_date=''
    e_date=''
    between_date = ""
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
        between_date = """and to_char(pt.server_created_on,'YYYY-MM-DD') >= '"""+s_date + \
            """' and to_char(pt.server_created_on,'YYYY-MM-DD') <= '""" + \
            e_date+"""' """
    phc_id=""
    if phc_ids:
        get_phc_name = PHC.objects.get(id=phc_ids)
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center_ids:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        sbc_ids = '''and sbc.id='''+sub_center
    village_id=""
    if village_ids:
        get_village_name = Village.objects.get(id=village_ids)
        village_id = '''and vlg.id='''+village
    cursor = connection.cursor()
    cursor.execute('''select phc.name as phc_name, sbc.name as sbc_name, vlg.name as village_name, 
    pt.name as patient_name, pt.patient_id as patient_code, pt.dob, date_part('year',age(pt.dob))::int as age, 
    case when pt.gender=1 then 'Male' when pt.gender=2 then 'Female' end as gender,
    case when trmt.bp_sys3!='' then trmt.bp_sys3 when trmt.bp_sys2!='' then trmt.bp_sys2 when trmt.bp_sys1!='' then trmt.bp_sys1 else '-' end as sbp,
    case when trmt.bp_non_sys3!='' then trmt.bp_non_sys3 when trmt.bp_non_sys2!='' then trmt.bp_non_sys2 when trmt.bp_non_sys1!='' then trmt.bp_non_sys1 else '-' end as dbp,
    trmt.fbs as fbs, trmt.pp as pp, trmt.random as random, ndc.name as diagnosis,
    case when dgs.source_treatment=1 then 'CLINIC' when dgs.source_treatment=2 then 'OUTSIDE' when dgs.source_treatment=3 then 'C&O' end as source_of_tretement,string_agg(md.name, ', ')
    from health_management_patients pt 
    inner join application_masters_village vlg on pt.village_id = vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id 
    inner join application_masters_phc phc on sbc.phc_id = phc.id
    left join health_management_treatments trmt on pt.uuid=trmt.patient_uuid
    left join health_management_prescription pst on trmt.patient_uuid=pst.patient_uuid
    left join application_masters_medicines md on pst.medicines_id=md.id
    left join health_management_diagnosis dgs on trmt.uuid=dgs.treatment_uuid
    left join application_masters_masterlookup ndc on dgs.ndc_id=ndc.id
    where 1=1 '''+phc_id+sbc_ids+village_id+between_date+''' 
    group by phc.name, sbc.name, vlg.name, pt.name, pt.patient_id, pt.dob, age, 
    source_of_tretement, ndc.name, gender, sbp, dbp, trmt.fbs, trmt.pp, trmt.random''')
    patient_data = cursor.fetchall()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="patient report '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['PATIENT REPORT'])
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village', 
            'Patient names', 
            'Patient code', 
            'DOB', 
            'Age', 
            'Gender', 
            'SBP', 
            'DBP', 
            'Blood sugar Fasting', 
            'Blood sugar pp', 
            'Blood sugar random', 
            'Diagnosis',
            'Source of treatment',
            'Treatment',
            ])
        for patient in patient_data:
            writer.writerow([
                patient[0],
                patient[1],
                patient[2],
                patient[3],
                patient[4],
                patient[5],
                patient[6],
                patient[7],
                patient[8],
                patient[9],
                patient[10],
                patient[11],
                patient[12],
                patient[13],
                patient[14],
                patient[15]
                ])
        return response
    data = pagination_function(request, patient_data)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/patient_registration_report.html', locals())


def patient_adherence_list(request):
    heading="PATIENTS ADHERENCE REPORT"
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    print(start_filter, 'start_filter')
    print(end_filter, 'end_filter')
    from datetime import date, timedelta
    import calendar
    last_day = date.today().replace(day=calendar.monthrange(date.today().year, date.today().month)[1])
    now = datetime.now()
    ed_filter = datetime.strftime(last_day,"%Y-%m-%d")
    sd_filter = now - relativedelta(months=2)
    sd_filter = sd_filter.strftime("%Y-%m")
    sd_filter = sd_filter+'-01'
    s_date=sd_filter
    e_date=ed_filter
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
    between_date = """and to_char(trmt.visit_date,'YYYY-MM-DD') >= '"""+s_date + \
        """' and to_char(trmt.visit_date,'YYYY-MM-DD') <= '""" + \
        e_date+"""' """
    phc_id=""
    if phc_ids:
        get_phc_name = PHC.objects.get(id=phc_ids)
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center_ids:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        sbc_ids = '''and sbc.id='''+sub_center
    village_id=""
    if village_ids:
        get_village_name = Village.objects.get(id=village_ids)
        village_id = '''and vlg.id='''+village
    # (extract(year from age('"""+e_date+"""','"""+s_date+"""'))*12 + extract(month from age('"""+e_date+"""','"""+s_date+"""')) + 1)::int as native_month
    cursor = connection.cursor()
    sql_query = """with a as (select phc.name as phc_name, sbc.name as sbc_name, vlg.name as village_name, pt.name as patient_name, pt.patient_id as patient_code, pt.uuid as pt_uuid, count(trmt.uuid) as no_of_time_clinics_held, 
    (extract(year from age('"""+e_date+"""','"""+s_date+"""'))*12 + extract(month from age('"""+e_date+"""','"""+s_date+"""'))+1)::int as native_month 
    from health_management_treatments trmt 
    inner join health_management_patients pt on trmt.patient_uuid = pt.uuid 
    inner join application_masters_village vlg on pt.village_id=vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id 
    inner join application_masters_phc phc on sbc.phc_id = phc.id where 1=1 """+phc_id+sbc_ids+village_id+between_date+""" group by phc_name, sbc_name, village_name, patient_name, patient_code, 
    pt.uuid order by vlg.name), b as 
    (select distinct(to_char(visit_date, 'YYYY-MM')) as date,patient_uuid as p_uuid from health_management_treatments trmt where 1=1 """+between_date+""" group by patient_uuid,visit_date)
    select phc_name, sbc_name, village_name, patient_name, patient_code, no_of_time_clinics_held, native_month, count(b.p_uuid) as month_count, 
    (case when native_month = 0 then 0 else round((count(b.p_uuid)/native_month::numeric)*100,0)end)::integer as per from a left join b on a.pt_uuid=b.p_uuid 
    group by phc_name, sbc_name, village_name, patient_name, patient_code, no_of_time_clinics_held, native_month, b.p_uuid"""
    cursor.execute(sql_query)
    patient_adherence_data = cursor.fetchall()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="patient adherence report '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['PATIENT ADHERENCE REPORT'])
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village', 
            'Patient names', 
            'Patient code', 
            'Number of time clinics held',
            "Expected number of days of Patient's attendance (A)",
            "Actual number of days of Patient's attendance (B)",
            '% of Patients adherence (B/A)%',
            ])
        for patient in patient_adherence_data:
            writer.writerow([
                patient[0],
                patient[1],
                patient[2],
                patient[3],
                patient[4],
                patient[5],
                patient[6],
                patient[7],
                patient[8]
                ])
        return response
    data = pagination_function(request, patient_adherence_data)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/patient_adherence.html', locals())


def utilisation_of_services_list(request):
    heading="UTILISATION OF SERVICES AT OBLF CLINICS"
    from dateutil.relativedelta import relativedelta
    filter_values = request.GET.dict()
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '0')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    s_date=''
    e_date=''
    between_date = ""
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
        between_date = """and to_char(pt.server_created_on,'YYYY-MM-DD') >= '"""+s_date + \
            """' and to_char(pt.server_created_on,'YYYY-MM-DD') <= '""" + \
            e_date+"""' """
    phc_id=""
    if phc_ids:
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        get_phc_name = PHC.objects.get(id=phc_ids)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center_ids:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        sbc_ids = '''and sbc.id='''+sub_center
    village_id=""
    if village_ids:
        get_village_name = Village.objects.get(id=village_ids)
        village_id = '''and vlg.id='''+village
    cursor = connection.cursor()
    cursor.execute('''with a as (select date(trmt.visit_date) as trmt_date, phc.name as phc_name, sbc.name as subcenter_name, vlg.name as village_name, 
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=1 then 1 else 0 end),0) as consultation_men_less_30, 
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=2 then 1 else 0 end),0) as consultation_female_less_30, 
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=1 then 1 else 0 end),0) as consultation_men_30_between_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=2 then 1 else 0 end),0) as consultation_female_30_between_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=1 then 1 else 0 end),0) as consultation_men_greater_50, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=2 then 1 else 0 end),0) as consultation_female_greater_50, 
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=1 and date(trmt.visit_date)=date(pt.registered_date) then 1 else 0 end),0) as treatment_men_less_30, 
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=2 and date(trmt.visit_date)=date(pt.registered_date) then 1 else 0 end),0) as treatment_female_less_30, 
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=1 and date(trmt.visit_date)=date(pt.registered_date) then 1 else 0 end),0) as treatment_men_30_between_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=2 and date(trmt.visit_date)=date(pt.registered_date) then 1 else 0 end),0) as treatment_female_30_between_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=1 and date(trmt.visit_date)=date(pt.registered_date) then 1 else 0 end),0) as treatment_men_greater_50, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=2 and date(trmt.visit_date)=date(pt.registered_date) then 1 else 0 end),0) as treatment_female_greater_50 
    from health_management_treatments trmt 
    inner join health_management_patients as pt on trmt.patient_uuid=pt.uuid 
    inner join application_masters_village vlg on pt.village_id = vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id 
    inner join application_masters_phc phc on sbc.phc_id = phc.id 
    where 1=1 '''+phc_id+sbc_ids+village_id+between_date+''' 
    group by phc.name, sbc.name, vlg.name, date(trmt.visit_date)) 
    select date(trmt_date), phc_name, subcenter_name, village_name, consultation_men_less_30, consultation_female_less_30, 
    consultation_men_30_between_50_age, consultation_female_30_between_50_age, consultation_men_greater_50, consultation_female_greater_50, 
    (consultation_men_less_30 + consultation_female_less_30 + consultation_men_30_between_50_age + consultation_female_30_between_50_age + consultation_men_greater_50 + consultation_female_greater_50) as consultation_total,
    treatment_men_less_30, treatment_female_less_30, 
    treatment_men_30_between_50_age, treatment_female_30_between_50_age, treatment_men_greater_50, treatment_female_greater_50, 
    (treatment_men_less_30 + treatment_female_less_30 + treatment_men_30_between_50_age + treatment_female_30_between_50_age + treatment_men_greater_50 + treatment_female_greater_50) as treatment_total
    from a''')
  
    utilisation_of_services_data = cursor.fetchall()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="Utilisation of services '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['UTILISATION OF SERVICES AT OBLF CLINICS'])
        writer.writerow([
            'Date',
            'PHC Name',
            'Sub Centre',
            'Village', 
            'Consultation <30 Men',
            'Consultation <30 women',
            'Consultation >=30 and <=50 Men',
            'Consultation >=30 and <=50 women',
            'Consultation >50 Men',
            'Consultation >50 women',
            'Consultation Total',
            'Treatment <30 Men',
            'Treatment <30 women',
            'Treatment >=30 and <=50 Men',
            'Treatment >=30 and <=50 women',
            'Treatment >50 Men',
            'Treatment >50 women',
            'Treatment Total',
            ])
        for data in utilisation_of_services_data:
            writer.writerow([
                data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
                data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17]
                ])
        return response 
    data = pagination_function(request, utilisation_of_services_data)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/utilisation_of_services.html', locals())



def prevelance_of_ncd_list(request):
    heading="Prevelance of NCD"
    filter_values = request.GET.dict()
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.GET.get('phc', '')
    sub_center = request.GET.get('sub_center', '')
    village = request.GET.get('village', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    start_filter = request.GET.get('start_filter', '')
    end_filter = request.GET.get('end_filter', '')
    s_date=''
    e_date=''
    between_date = ""
    if start_filter != '':
        s_date = start_filter
        e_date = end_filter
        between_date = """and to_char(pt.server_created_on,'YYYY-MM-DD') >= '"""+s_date + \
            """' and to_char(pt.server_created_on,'YYYY-MM-DD') <= '""" + \
            e_date+"""' """
    phc_id= ""
    if phc:
        get_phc_name = PHC.objects.get(id=phc_ids)
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center:
        get_sbc_name = Subcenter.objects.get(id=sub_center_ids)
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        sbc_ids = '''and sbc.id='''+sub_center
    village_id=""
    if village_ids:
        get_village_name = Village.objects.get(id=village_ids)
        village_id = '''and vlg.id='''+village
    
    cursor = connection.cursor()
    cursor.execute('''with a as (select phc.name as phc_name, sbc.name as sbc_name, vlg.name as vlg_name,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=1 then 1 else 0 end),0) as men_less_30,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=2 then 1 else 0 end),0) as female_less_30,
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=1 then 1 else 0 end),0) as men_30_between_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=2 then 1 else 0 end),0) as female_30_between_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=1 then 1 else 0 end),0) as men_greater_50, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=2 then 1 else 0 end),0) as female_greater_50,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=1 and date(pt.registered_date)=date(trmt.visit_date) then 1 else 0 end),0) as new_men_less_30,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=2 and date(pt.registered_date)=date(trmt.visit_date) then 1 else 0 end),0) as new_female_less_30,
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=1 and date(pt.registered_date)=date(trmt.visit_date) then 1 else 0 end),0) as new_men_30_between_50_age,
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=2 and date(pt.registered_date)=date(trmt.visit_date) then 1 else 0 end),0) as new_female_30_between_50_age,
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=1 and date(pt.registered_date)=date(trmt.visit_date) then 1 else 0 end),0) as new_men_greater_50, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=2 and date(pt.registered_date)=date(trmt.visit_date) then 1 else 0 end),0) as new_female_greater_50
    from health_management_patients pt 
    inner join application_masters_village vlg on pt.village_id = vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id 
    inner join application_masters_phc phc on sbc.phc_id = phc.id 
    inner join health_management_treatments as trmt on pt.uuid = trmt.patient_uuid 
    inner join health_management_diagnosis as dgn on trmt.uuid = dgn.treatment_uuid 
    inner join application_masters_masterlookup mtk on dgn.ndc_id = mtk.id
    where 1=1 '''+phc_id+sbc_ids+village_id+between_date+'''
    group by phc.name, sbc.name, vlg.name order by vlg.name) select phc_name, sbc_name, vlg_name, men_less_30,
    female_less_30, men_30_between_50_age, female_30_between_50_age, men_greater_50, female_greater_50, 
    (men_less_30 + female_less_30 + men_30_between_50_age + female_30_between_50_age + men_greater_50 + female_greater_50)
    as ncd_total, new_men_less_30, new_female_less_30, new_men_30_between_50_age, new_female_30_between_50_age, new_men_greater_50, new_female_greater_50, (new_men_less_30 + new_female_less_30 + new_men_30_between_50_age + new_female_30_between_50_age + new_men_greater_50 + new_female_greater_50) as new_ncd_total from a''')
    prevelance_of_ncd_data = cursor.fetchall()
    export_flag = True if request.POST.get('export') and request.POST.get( 'export').lower() == 'true' else False
    if export_flag:
        response = HttpResponse(content_type='text/csv',)
        response['Content-Disposition'] = 'attachment; filename="prevelance of ncd '+ str(localtime(timezone.now()).strftime("%m-%d-%Y %I-%M %p")) +'.csv"'
        writer = csv.writer(response)
        writer.writerow(['PREVELANCE OF NCD'])
        writer.writerow([
            'PHC Name',
            'Sub Centre',
            'Village', 
            '<30 Men NCD',
            '<30 women NCD',
            '>=30 and <=50 Men NCD',
            '>=30 and <=50 women NCD',
            '>50 Men NCD',
            '>50 women NCD',
            'Total NCD',
            '<30 Men New NCD',
            '<30 women New NCD',
            '>=30 and <=50 Men New NCD',
            '>=30 and <=50 women New NCD',
            '>50 Men New NCD',
            '>50 women New NCD',
            'Total New NCD',
            ])
        for data in prevelance_of_ncd_data:
            writer.writerow([
                data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],
                data[10],data[11],data[12],data[13],data[14],data[15],data[16]
                ])
        return response
    data = pagination_function(request, prevelance_of_ncd_data  )
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/prevelance_of_ncd.html', locals())

def get_sub_center(request, subcenter_id):
    if request.method == 'GET' and request.is_ajax():
        result_set = []
        sub_centers = Subcenter.objects.filter(status=2, phc__id=subcenter_id)
        for sub_center in sub_centers:
            result_set.append(
                {'id': sub_center.id, 'name': sub_center.name,})
        return HttpResponse(json.dumps(result_set))

def get_village(request, village_id):
    if request.method == 'GET' and request.is_ajax():
        result_set = []
        villages = Village.objects.filter(status=2, subcenter__id=village_id)
        for village in villages:
            result_set.append(
                {'id': village.id, 'name': village.name,})
        return HttpResponse(json.dumps(result_set))

def add_medicine_stock(request):
    heading="Add medicine stocks details"
    search = request.GET.get('search', '')
    if search:
        medicine = Medicines.objects.filter(name__icontains=search)
    else:
        medicine = Medicines.objects.filter(status=2)
    now = datetime.now()
    current_data = now.strftime("%Y-%m-%d")
    if request.method == 'POST':
        data = request.POST
        for mdn in medicine:
            no_of_units = data.get(str(mdn.id)+'_no_of_units')
            if no_of_units:
                no_of_units = no_of_units
                unit_price = data.get(str(mdn.id)+'_unit_price')
                opening_stock = data.get(str(mdn.id)+'_opening_stock')
                date_of_creation = data.get(str(mdn.id)+'_date_of_creation')
                closing_stock = data.get(str(mdn.id)+'_closing_stock')
                medicine_stock = MedicineStock.objects.create(medicine=mdn, date_of_creation=date_of_creation or None, 
                unit_price=unit_price or None, no_of_units=no_of_units or None, opening_stock=opening_stock or None, closing_stock=closing_stock or None)    
                medicine_stock.save()
        return redirect('/medicine/list/')
    return render(request, 'manage_stocks/medicine_stock/add_medicine.html', locals())

def user_add(request):
    heading='userprofile'
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phonenumber')
            user_role = request.POST.get('user_role', '')
            village_name = request.POST.getlist('village_name', '')
            if User.objects.filter(username=username).exists():
                user_exist="Username already exists"
                return render(request, 'user/add_user.html', locals())
            user=User.objects.create_user(username=username,password=password, first_name=name, email=email)
            user_profile=UserProfile.objects.create(user=user, phone_no=phonenumber, user_type=user_role)
            user_profile.village.add(*village_name)
            user_profile.save()
            return redirect('/list/userprofile/')
        except:
            user.delete()
            error="User is not created. Please try again."  
    village_names=Village.objects.filter(status=2).order_by('name')  
    user_type_chooces=UserProfile.USER_TYPE_CHOICES
    return render(request, 'user/add_user.html', locals())

def user_edit(request,id):
    heading='userprofile'
    user_profile=UserProfile.objects.get(id=id)
    user_profiles=UserProfile.objects.filter(id=id)
    user_profiles_village = user_profiles.values_list('village__id', flat=True)
    user_obj = User.objects.get(id=user_profile.user.id)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        village_name = request.POST.getlist('village_name', '')
        user_role = request.POST.get('user_role', '')
        user_obj.first_name=name
        user_obj.email=email
        user_obj.save()
        user_profile.phone_no=phonenumber
        user_profile.user_type=user_role
        user_profile.village.clear()
        user_profile.village.add(*village_name)
        user_profile.user.set_password(password)
        user_profile.save()
        return redirect('/list/userprofile/')
    village_names=Village.objects.filter(status=2).order_by('name')  
    user_type_chooces=UserProfile.USER_TYPE_CHOICES
    return render(request, 'user/add_user.html', locals())


def master_add_form(request,model):
    if model == 'masterlookup':
        heading='diagnosis'
    else:
        heading=model
    user_form = eval(model.title()+'Form') 
    forms=user_form()

    if request.method == 'POST':
        fields = user_form(request.POST)
        if fields.is_valid():
            fields.save()
            return redirect('/list/'+str(model))
    return render(request, 'user/master_edit_form.html', locals())


def master_edit_form(request,model,id):
    if model == 'masterlookup':
        heading='diagnosis'
    else:
        heading=model
    if model != 'userprofile':
        listing_model = apps.get_model(app_label= 'application_masters', model_name=model)
    else:
        listing_model = apps.get_model(app_label= 'health_management', model_name=model)
    obj=listing_model.objects.get(id=id)
    user_form = eval(model.title()+'Form') 
    
    forms=user_form(request.POST or None,instance=obj)
    if request.method == 'POST' and forms.is_valid():
        forms.save()
        return redirect('/list/'+str(model))
    return render(request, 'user/master_edit_form.html', locals())

def delete_record(request,model,id):
    if model != 'userprofile':
        listing_model = apps.get_model(app_label= 'application_masters', model_name=model)
    else:
        listing_model = apps.get_model(obj= 'health_management', model_name=model)
    obj=listing_model.objects.get(id=id)#.update(status=1)
    if obj.status == 2:
        obj.status=1
    else:
        obj.status=2
    obj.save()
    return redirect('/list/'+str(model))

# from django.db.models import Q
def master_list_form(request,model):
    search = request.GET.get('search', '')
    headings={
        "userprofile":"user profile",
        "masterlookup":"diagnosis",
    }
    heading=headings.get(model,model)
    orderlist='name' if model != 'userprofile' else 'user__username'
    if model != 'userprofile':
        listing_model = apps.get_model(app_label= 'application_masters', model_name=model)
    else:
        listing_model = apps.get_model(app_label= 'health_management', model_name=model)
    objects=listing_model.objects.all().order_by(orderlist)#.values_list('id','name',named=True)
    if model == 'masterlookup':
        objects=listing_model.objects.filter(parent__id=4).order_by(orderlist)

     
    if search and model == 'userprofile':
        objects=objects.filter(user__username__icontains=search)
    elif search:
        objects=objects.filter(name__icontains=search)

    data = pagination_function(request, objects)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'user/master_list_form.html', locals())

class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        user = None
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if email:
            try:
                findUser = UserProfile._default_manager.get(
                    user__email__iexact=email) 
                user = findUser.user
            except UserProfile.DoesNotExist:
                findUser = None
        elif username:
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
        create_post_log(request,data)
        data = request.data
        create_post_log(request,data)
        try:
            valid_user = UserProfile.objects.get(uuid = pk)
        except:
            return Response({"message":"Invalid UUID"})
        if valid_user:
            patient_visit_type=MasterLookup.objects.filter(parent__id=6)
            user_list = UserProfile.objects.filter(uuid = pk)
            if valid_user.user_type == 1:
                user_wise_village_ids = user_list.values_list('village__id', flat=True)
                village=Village.objects.filter(status=2, id__in=user_wise_village_ids).order_by('id')
                subcenter_ids=village.values_list('subcenter__id')
                subcenter=Subcenter.objects.filter(status=2, id__in=subcenter_ids).order_by('id')
                phc_ids=subcenter.values_list('phc__id')
                phc=PHC.objects.filter(status=2, id__in=phc_ids).order_by('id')  
                patient_smo_date = Patients.objects.filter(status=2, village__id__in=user_wise_village_ids, patient_visit_type__in=patient_visit_type).order_by('server_modified_on') 
            else:
                village=Village.objects.filter(status=2).order_by('id')
                subcenter=Subcenter.objects.filter(status=2).order_by('id')   
                phc=PHC.objects.filter(status=2).order_by('id')   
                patient_smo_date = Patients.objects.filter(status=2, patient_visit_type__in=patient_visit_type).order_by('server_modified_on')

            phcserializers=PHCSerializers(phc, many=True)
            villagesites_serializer=VillageSerializers(village, many=True)
            subcenterserializers=SubcenterSerializers(subcenter, many=True)

            #State
            state=State.objects.filter(status=2).order_by('id')
            stateserializer=StateSerializers(state, many=True)

            #district
            district=District.objects.filter(status=2).order_by('id')   
            districtserializers=DistrictSerializers(district, many=True)

            #taluk
            taluk=Taluk.objects.filter(status=2).order_by('id')   
            talukserializers=TalukSerializers(taluk, many=True) 

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
            userprofileserializer=UserProfileSerializers(user_list, many=True)

            # patient data
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
            prescription_smo_date = Prescription.objects.filter(status=2, treatment_uuid__in=patient_treatment_uuids).order_by('server_modified_on')
            if data.get('prescription_smo_date'):
                prescription_smo_date = prescription_smo_date.filter(server_modified_on__gt = data.get('prescription_smo_date'))
            prescriptionserializers = PrescriptionSerializers(prescription_smo_date,many=True)

            #diagnosis
            ndcs=MasterLookup.objects.filter(parent__id=4)
            diagnosis_smo_date = Diagnosis.objects.filter(status=2, treatment_uuid__in=patient_treatment_uuids, ndc__in=ndcs).order_by('server_modified_on')
            if data.get('diagnosis_smo_date'):
                diagnosis_smo_date = diagnosis_smo_date.filter(server_modified_on__gt = data.get('diagnosis_smo_date'))
            diagnosisserializers = DiagnosisSerializers(diagnosis_smo_date,many=True)

            # scanned report
            scanned_report_smo_date = Scanned_Report.objects.filter(status=2, patient_uuid__in=patient_uuids).order_by('server_modified_on')
            if data.get('scanned_report_smo_date'):
                scanned_report_smo_date = scanned_report_smo_date.filter(server_modified_on__gt = data.get('scanned_report_smo_date'))
            scanned_reportserializers = ScannedReportSerializers(scanned_report_smo_date,many=True)

            # home visit
            home_visit_smo_date = HomeVisit.objects.filter(status=2,patient_uuid__in=patient_uuids).order_by('server_modified_on')
            home_visit_uuids=home_visit_smo_date.values_list('uuid',flat=True)
            if data.get('home_visit_smo_date'):
                home_visit_smo_date= home_visit_smo_date.filter(server_modified_on__gt = data.get('treatment_smo_date'))
            home_visit_serializers = HomeVisitSerializers(home_visit_smo_date,many=True)

            jsonresponse_full = {
                "status":2,
                "message":"Data Already Sent",
            } 
            jsonresponse_full['villages'] = villagesites_serializer.data
            jsonresponse_full['state'] = stateserializer.data
            jsonresponse_full['district'] = districtserializers.data
            jsonresponse_full['taluk'] = talukserializers.data
            jsonresponse_full['phc'] = phcserializers.data
            jsonresponse_full['subcenter'] = subcenterserializers.data
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
            jsonresponse_full['home_visit'] = home_visit_serializers.data

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
        home_visit_success =[]
        try:
            data = request.build_absolute_uri()
            # create_post_log(request,data)
            data = request.data
            # create_post_log(request,data)
            # import ipdb
            # ipdb.set_trace()
            patient_response = {'data':[]}
            diagnosis_response = {'data':[]}
            prescription_response = {'data':[]}
            treatment_response = {'data':[]}
            scanned_report_response = {'data':[]}
            home_visit_response = {'data':[]}

            try:
                valid_user = UserProfile.objects.filter(uuid = pk)
            except:
                return Response({"message":"Invalid UUID"})
            #-TODO-valid user based on that village
            if  valid_user :
                user = valid_user.first()
                with transaction.atomic():
                    # user_data = data.get('userdata')
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
                    
                    home_visit_data  = home_visit_details(request)
                    for obj in home_visit_data:
                        home_visit_info ={}
                        home_visit_info['uuid']=obj.uuid
                        home_visit_info['SCO'] = obj.server_created_on
                        home_visit_info['SMO'] = obj.server_modified_on
                        home_visit_info['sync_status'] = obj.sync_status
                        home_visit_response['data'].append(home_visit_info)
                        home_visit_success =  home_visit_response['data']



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
                "home_visit_data" : home_visit_success,
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
                "home_visit_data" : home_visit_success,
            })
    
def patient_details(self):
    objlist =[]
    datas = json.loads(self.data.get('patients'))
    create_post_log(self,datas)
    for data in datas:
        obj, created = Patients.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
            defaults= {
                        "name" : data.get('name'),
                        "dob" : data.get('dob'),
                        "age":data.get('age'),
                        "gender" : data.get('gender'),
                        "village_id" : data.get('village_id') if data.get('village_id') != 0 else None,
                        "subcenter_id" : data.get('subcenter_id') if data.get('subcenter_id') != '' else None,
                        "phone_number": data.get('phone'),
                        "height":data.get('height'),
                        "weight":data.get('weight') if data.get('weight') != '' else None,
                        "door_no":data.get('door_no') if data.get('weight') != '' else None,
                        "seq_no":data.get('seq_no') if data.get('weight') != '' else None,
                        "patient_visit_type_id": data.get('patient_visit_type'),                        
                        "fee_status":data.get('fee_status'),
                        "fee_paid":data.get('fee_paid'),
                        "fee_date":data.get('fee_date'),
                        "registered_date":data.get('registered_date'),
                        "last_visit_date":data.get('last_visit_date'),
                        })
        if created:
            obj.patient_id = data.get('patient_id')
        if self.FILES.get(data.get('uuid')):
            obj.image=self.FILES.get(data.get('uuid'))
        obj.save()
        
        objlist.append(obj)

    return objlist


def treatment_details(self):
    objlist = []
    datas = json.loads(self.get('treatment'))
    create_post_log(self,datas)
    for data in datas:
        obj,created = Treatments.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
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
    datas = json.loads(self.get('prescription'))
    create_post_log(self,datas)
    for data in datas:
        obj,created = Prescription.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
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
    datas = json.loads(self.get('diagnosis'))
    create_post_log(self,datas)
    for data in datas:
        obj,created = Diagnosis.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
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
    datas = json.loads(self.get('scanned_report'))
    create_post_log(self,datas)
    for data in datas:
        obj,created = Scanned_Report.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
            patient_uuid = data.get('patient_uuid'),

            defaults = {
                    "title" : data.get('title'),
                    "image_path" : data.get('image_path'),
                    "captured_date" : data.get('captured_date'),
                    })
        objlist.append(obj)

    return objlist


def home_visit_details(self):
    objlist = []
    datas = json.loads(self.data.get('home_visit'))
    create_post_log(self,datas)
    for data in datas:
        obj,created = HomeVisit.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
            defaults = {
                    "patient_uuid" : data.get('patient_uuid'),
                    "home_vist" : data.get('home_vist'),
                    "image_location" : data.get('image_location'),
                    "response_location" : data.get('response_location'),
                    "response_datetime" : data.get('response_datetime'),
                    })
        objlist.append(obj)
        if self.FILES.get(data.get('uuid')):
            obj.image=self.FILES.get(data.get('uuid'))
        obj.save()
    return objlist

import os
# from datetime import datetime
def create_post_log(request,data):
    from OBLH_HM.settings import BASE_DIR
    from django.core.files.base import ContentFile, File
    today_date = datetime.now()
    year = today_date.strftime("%Y")
    dt = today_date.strftime("%d")
    m = today_date.strftime("%m")
    hour = today_date.strftime("%H")
    minute = today_date.strftime("%M")
    new_file_path = '%s/media/logSync/%s/%s/%s' % (BASE_DIR,year,m,dt)
    if not os.path.exists(new_file_path):
        os.makedirs(new_file_path)
    file_name = "SyncLog" + "-" + year + "-" + m + "-" + dt + ".txt"
    full_filename = os.path.join(BASE_DIR,new_file_path,file_name)
    with open(full_filename, 'a', encoding='utf8') as f:
        f.writelines("\n\n\n==================================================\n\n")
        f.writelines("\nLog Date & Time : "+ datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+"hrs")
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()
    return True

        


  


  
