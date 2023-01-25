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
    response['Content-Disposition'] = 'attachment; filename="Drug prescription'+ str(localtime(timezone.now()).strftime("%m/%d/%Y %I:%M %p")) +'.csv"'
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

def patient_csv_export(request):
    response = HttpResponse(content_type='text/csv',)
    response['Content-Disposition'] = 'attachment; filename="patient registeration'+ str(localtime(timezone.now()).strftime("%m/%d/%Y %I:%M %p")) +'.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'PHC Name',
        'Sub Centre',
        'Village', 
        'Patient names', 
        'Age', 
        'DOB', 
        'Gender', 
        'Date of registration', 
        'Health Worker', 
        'Created On', 
        ])
    patients_csv = Patients.objects.filter()
    for patient in patients_csv:
        health_worker = patient.get_health_worker()
        diagnosis = patient.get_diagnosis_id()
        writer.writerow([
            patient.village.subcenter.phc if patient.village else '',
            patient.village.subcenter if patient.village else '',
            patient.village if patient else '',
            patient.name,
            patient.age,
            patient.dob,
            patient.get_gender_display(),
            patient.registered_date,
            diagnosis.source_treatment if diagnosis else '',
            health_worker.user.first_name if health_worker else '', 
            patient.server_created_on.strftime("%m/%d/%Y %I:%M %p"),
             ])
    return response

def distribution_village_wise_csv(request):
    response = HttpResponse(content_type='text/csv',)
    response['Content-Disposition'] = 'attachment; filename="distribution village wise medicine'+ str(localtime(timezone.now()).strftime("%m/%d/%Y %I:%M %p")) +'.csv"'
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


def medicine_report_list(request):
    heading="DISTRIBUTION OF MEDICINE"
    search = request.GET.get('search', '')
    if search:
        medicine_stock = Medicines.objects.filter(name__icontains=search)
    else:
        medicine_stock = Medicines.objects.filter(status=2)
    data = pagination_function(request, medicine_stock)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/medicine_qty_report.html', locals())


def distribution_village_wise_medicine_report_list(request):
    heading="DISTRIBUTION OF MEDICINE - VILLAGE-WISE REPORT"
    medicine_obj=Medicines.objects.filter(status=2)
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.POST.get('phc', '')
    sub_center = request.POST.get('sub_center', '')
    village = request.POST.get('village', '')
    medicine = request.POST.get('medicine', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    medicine_ids = int(medicine) if medicine != '' else ''
    start_filter = request.POST.get('start_filter', '')
    end_filter = request.POST.get('end_filter', '')
    s_date=''
    e_date=''
    medicine_list = True
    distribution_list=Prescription.objects.filter(status=2)
    if start_filter != '':
        start_date = start_filter+'-01'
        end_date = end_filter+'-01'
        sd_date= datetime.strptime(start_date, "%Y-%m-%d")
        ed_date= datetime.strptime(end_date, "%Y-%m-%d")
        ed_date = ed_date + relativedelta(months=1)
        s_date = sd_date.strftime("%Y-%m-%d")
        e_date = ed_date.strftime("%Y-%m-%d")
        distribution_list=distribution_list.filter(status=2, server_created_on__range=[s_date,e_date])
    if phc_ids:
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        pateint_registration_report = Patients.objects.filter(village__subcenter__phc__id=phc_ids).values_list('uuid')
        distribution_list = distribution_list.filter(patient_uuid__in=pateint_registration_report)
    if sub_center_ids:
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        pateint_registration_report = Patients.objects.filter(village__subcenter__id=sub_center_ids).values_list('uuid')
        distribution_list = distribution_list.filter(patient_uuid__in=pateint_registration_report)
    if village_ids:
        pateint_registration_report = Patients.objects.filter(village__id=village_ids).values_list('uuid')
        distribution_list = distribution_list.filter(patient_uuid__in=pateint_registration_report)
    if medicine_ids:
        distribution_list = distribution_list.filter(medicines__id=medicine_ids)


    data = pagination_function(request, distribution_list)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/village_wise_report.html', locals())

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
    medicine_obj=Medicines.objects.filter(status=2)
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.POST.get('phc', '')
    sub_center = request.POST.get('sub_center', '')
    village = request.POST.get('village', '')
    medicine = request.POST.get('medicine', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    medicine_ids = int(medicine) if medicine != '' else ''
    start_filter = request.POST.get('start_filter', '')
    end_filter = request.POST.get('end_filter', '')
    s_date=''
    e_date=''
    medicine_list = True
    prescription_list=Prescription.objects.filter(status=2)
    if start_filter != '':
        start_date = start_filter+'-01'
        end_date = end_filter+'-01'
        sd_date= datetime.strptime(start_date, "%Y-%m-%d")
        ed_date= datetime.strptime(end_date, "%Y-%m-%d")
        ed_date = ed_date + relativedelta(months=1)
        s_date = sd_date.strftime("%Y-%m-%d")
        e_date = ed_date.strftime("%Y-%m-%d")
        prescription_list=prescription_list.filter(status=2, server_created_on__range=[s_date,e_date])
    if phc_ids:
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        pateint_registration_report = Patients.objects.filter(village__subcenter__phc__id=phc_ids).values_list('uuid')
        prescription_list = prescription_list.filter(patient_uuid__in=pateint_registration_report)
    if sub_center_ids:
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        pateint_registration_report = Patients.objects.filter(village__subcenter__id=sub_center_ids).values_list('uuid')
        prescription_list = prescription_list.filter(patient_uuid__in=pateint_registration_report)
    if village_ids:
        pateint_registration_report = Patients.objects.filter(village__id=village_ids).values_list('uuid')
        prescription_list = prescription_list.filter(patient_uuid__in=pateint_registration_report)
    if medicine_ids:
        prescription_list = prescription_list.filter(medicines__id=medicine_ids)


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
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    health_worker_obj = UserProfile.objects.filter(status=2, user_type=1).distinct('user__first_name').order_by('user__first_name').exclude(user__first_name__exact='')
    phc = request.POST.get('phc', '')
    sub_center = request.POST.get('sub_center', '')
    village = request.POST.get('village', '')
    health_worker = request.POST.get('health_worker', '')
    phc_ids = int(phc) if phc != '' else ''
    sub_center_ids = int(sub_center) if sub_center != '' else ''
    village_ids = int(village) if village != '' else ''
    health_worker_ids = int(health_worker) if health_worker != '' else ''
    start_filter = request.POST.get('start_filter', '')
    end_filter = request.POST.get('end_filter', '')
    s_date=''
    e_date=''
    pateint_registration_report = Patients.objects.filter(status=2)
    health_worker_in_patient = True
    if start_filter != '':
        start_date = start_filter+'-01'
        end_date = end_filter+'-01'
        sd_date= datetime.strptime(start_date, "%Y-%m-%d")
        ed_date= datetime.strptime(end_date, "%Y-%m-%d")
        ed_date = ed_date + relativedelta(months=1)
        s_date = sd_date.strftime("%Y-%m-%d")
        e_date = ed_date.strftime("%Y-%m-%d")
        pateint_registration_report = Patients.objects.filter(status=2, server_created_on__range=[s_date,e_date])   
    if health_worker_ids:
        health_worker = UserProfile.objects.filter(status=2, user__id=health_worker).values_list('uuid', flat=True)
        pateint_registration_report = pateint_registration_report.filter(user_uuid__in=health_worker)
    if phc_ids:
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc_ids)
        pateint_registration_report = pateint_registration_report.filter(village__subcenter__phc__id=phc_ids)
    if sub_center_ids:
        village_obj = Village.objects.filter(status=2, subcenter__id=sub_center_ids)
        pateint_registration_report = pateint_registration_report.filter(village__subcenter__id=sub_center_ids)
    if village_ids:
        pateint_registration_report = pateint_registration_report.filter(village__id=village_ids)


    data = pagination_function(request, pateint_registration_report)
    current_page = request.GET.get('page', 1)
    page_number_start = int(current_page) - 2 if int(current_page) > 2 else 1
    page_number_end = page_number_start + 5 if page_number_start + \
        5 < data.paginator.num_pages else data.paginator.num_pages+1
    display_page_range = range(page_number_start, page_number_end)
    return render(request, 'reports/patient_registration_report.html', locals())

def phc_wise_patient_export_csv(request):
    response = HttpResponse(content_type='text/csv',)
    response['Content-Disposition'] = 'attachment; filename="distribution village wise medicine'+ str(localtime(timezone.now()).strftime("%m/%d/%Y %I:%M %p")) +'.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'PHC Name',
        'Sub Centre',
        'Village', 
        '<30 Men',
        '<30 women',
        '>=30 and <=50 Men',
        '>=30 and <=50 women',
        '>50 Men',
        '>50 women',
        'Total',
        ])
    phc_wise_csv = phc_wise_sql_data(phc_ids, sbc_ids, village_ids, between_date)
    for data in phc_wise_csv:
        writer.writerow([
            data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]
            ])
    return response 


def phc_wise_sql_data(phc_ids, sbc_ids, village_ids, between_date):
    cursor = connection.cursor()
    cursor.execute('''with a as (select phc.name as phc_name, sbc.name as sbc_name, vlg.name as vlg_name,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=1 then 1 else 0 end),0) as men_greater_30,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=2 then 1 else 0 end),0) as female_greater_30,
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=1 then 1 else 0 end),0) as men_between_30_50_age,
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=2 then 1 else 0 end),0) as female_between_30_50_age,
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=1 then 1 else 0 end),0) as men_above_50,
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=2 then 1 else 0 end),0) as female_above_50
    from health_management_patients
    inner join application_masters_village vlg on health_management_patients.village_id = vlg.id
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id
    inner join application_masters_phc phc on sbc.phc_id = phc.id
    where 1=1 '''+phc_ids+sbc_ids+village_ids+''' 
    group by village_id, phc.name, sbc.name, vlg.name)
    select phc_name, sbc_name, vlg_name, men_greater_30,female_greater_30, men_between_30_50_age, female_between_30_50_age, men_above_50, female_above_50,
    (men_greater_30 + female_greater_30 + men_between_30_50_age + female_between_30_50_age + men_above_50 + female_above_50)
    as total from a 
    ''')
    data = cursor.fetchall()
    return data


def phc_wise_patient_list(request):
    heading="Patient Registration Report"
    from dateutil.relativedelta import relativedelta
    phc_obj = PHC.objects.filter(status=2)
    phc = request.POST.get('phc', '')
    sub_center = request.POST.get('sub_center', '')
    village = request.POST.get('village', '')
    start_filter = request.POST.get('start_filter', '')
    end_filter = request.POST.get('start_filter', '')
    s_date=''
    e_date=''
    between_date = ""
    if start_filter != '':
        start_date = start_filter+'-01'
        end_date = end_filter+'-01'
        sd_date= datetime.strptime(start_date, "%Y-%m-%d")
        ed_date= datetime.strptime(end_date, "%Y-%m-%d")
        ed_date = ed_date + relativedelta(months=1)
        s_date = sd_date.strftime("%Y-%m-%d")
        e_date = ed_date.strftime("%Y-%m-%d")
        between_date = '''and server_created_on BETWEEN '''+str(s_date)+''' and '''+str(e_date)
    phc_ids= ""
    if phc:
        sub_center_obj = Subcenter.objects.filter(status=2, phc__id=phc)
        phc_id = '''and phc.id='''+phc
    sbc_ids= ""
    if sub_center:
        sbc_ids = '''and sbc.id='''+sub_center
    village_ids=""
    if village:
        village_obj = Village.objects.filter(status=2, subcenter__id=village)
        village_ids = '''and vlg.id='''+village
    
    data = phc_wise_sql_data(phc_ids, sbc_ids, village_ids, between_date)
    # data = phc_wise_patient_export_csv(phc_ids, sbc_ids)
    return render(request, 'reports/phc_wise_patient_list.html', locals())

def disease_sql_data(request):
    cursor = connection.cursor()
    cursor.execute('''with a as (select phc.name as phc_name, sbc.name as sbc_name, vlg.name as vlg_name, mtk.name as mtk_name,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=1 then 1 else 0 end),0) as men_greater_30,
    coalesce(sum(case when date_part('year',age(dob))<30 and gender=2 then 1 else 0 end),0) as female_greater_30,
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=1 then 1 else 0 end),0) as men_between_30_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>=30 and date_part('year',age(dob))<=50 and gender=2 then 1 else 0 end),0) as female_between_30_50_age, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=1 then 1 else 0 end),0) as men_above_50, 
    coalesce(sum(case when date_part('year',age(dob))>50 and gender=2 then 1 else 0 end),0) as female_above_50
    from health_management_patients pt 
    inner join application_masters_village vlg on pt.village_id = vlg.id 
    inner join application_masters_subcenter sbc on vlg.subcenter_id = sbc.id 
    inner join application_masters_phc phc on sbc.phc_id = phc.id 
    inner join health_management_treatments as trmt on pt.uuid = trmt.patient_uuid 
    inner join health_management_diagnosis as dgn on trmt.uuid = dgn.treatment_uuid 
    inner join application_masters_masterlookup mtk on dgn.ndc_id = mtk.id 
    group by village_id, phc.name, sbc.name, vlg.name, mtk.name) select phc_name, sbc_name, vlg_name, mtk_name, men_greater_30,
    female_greater_30, men_between_30_50_age, female_between_30_50_age, men_above_50, female_above_50, 
    (men_greater_30 + female_greater_30 + men_between_30_50_age + female_between_30_50_age + men_above_50 + female_above_50)
    as total from a''')
    data = cursor.fetchall()
    return render(request, 'reports/phc_village_wise_disease_report.html', locals())

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
            data = request.data
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
    # import ipdb
    # ipdb.set_trace()
    for data in json.loads(self.data.get('patients')):
        # print(type(data.get('village_id')))
        obj, created = Patients.objects.update_or_create(
            uuid = data.get('uuid'),
            user_uuid = data.get('user_uuid'),
            defaults= {
                        "name" : data.get('name'),
                        "dob" : data.get('dob'),
                        "age":data.get('age'),
                        "gender" : data.get('gender'),
                        "village_id" : data.get('village_id') if data.get('village_id') != 0 else None,
                        # "village__phc_id" : data.get('phc_id'),
                        # "state_id" : data.get('state_id'),
                        # "district_id" : data.get('district_id'),
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

    for data in json.loads(self.get('treatment')):
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
    for data in json.loads(self.get('prescription')):
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
    for data in json.loads(self.get('diagnosis')):
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
    for data in json.loads(self.get('scanned_report')):
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
    for data in json.loads(self.data.get('home_visit')):
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



        


  


  
