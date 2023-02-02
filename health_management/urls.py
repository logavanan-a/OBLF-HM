from django.contrib import admin
from django.urls import path
from health_management.views import *
from .forms import *


app_name = "health_management"

urlpatterns = [
    path('', login_view, name="login"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('app-login/', LoginAPIView.as_view()),
    path('phc/pull/<pk>/', Phc_pull.as_view()),
    path('phc/push/<pk>/', Phc_push.as_view()),

    path('patient-csv-export/', patient_csv_export, name='patient_csv_export'),

    path('disease/report/', phc_village_wise_disease_list, name='phc_village_wise_disease_list'),
    path('home-visit/report/', home_visit_report, name='home_visit_report'),
    path('phc-wise-patient/report/', phc_wise_patient_list, name='phc_wise_patient_list'),
    path('patient-registration/report/', patient_registration_report, name='patient_registration_report'),
    path('village-wise-medicine/report/', distribution_village_wise_medicine_report_list, name='village_wise_drug_list'),
    path('drug-dispensation/report/', drug_dispensation_stock_list, name='drug_dispensation_stock_list'),

    path('village-wise-drugs/list/', village_wise_drugs_list, name='village_wise_drug_list'),
    path('add/village-wise-drugs/', add_village_wise_drugs, name='add_village_wise_drugs'),

    path('medicine/list/', medicine_stock_list, name='medicine_stock_list'),
    path('add/medicine/', add_medicine_stock, name='add_medicine_stock'),


    path('ajax/subcenter/<subcenter_id>/', get_sub_center, name="subcenter"),
    path('ajax/village/<village_id>/', get_village, name="village"),


    path('add/userprofile/', user_add),
    path('edit/userprofile/<id>/', user_edit),
    path('list/<model>/', master_list_form),
    path('add/<model>/', master_add_form),
    path('edit/<model>/<id>/', master_edit_form),
    path('<model>/<id>/delete/', delete_record,name='delete_record'),
	# path('mhu/push/<pk>/', Mhu_push.as_view()),

]