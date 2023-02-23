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

    #verfied report
    path('verified-diagnosis-report/', verified_diagnosis_report, name='verified_diagnosis'),
    path('verified-home-visit-report/', verified_home_visit_report, name='verified_home_visit_report'),
    path('verified-treatments-report/', verified_treatments_report, name='verified_treatments_report'),


    path('prevelance-of-ncd/report/', prevelance_of_ncd_list, name='prevelance_of_ncd_list'),
    path('home-visit/report/', home_visit_report, name='home_visit_report'),
    path('utilisation-of-services/report/', utilisation_of_services_list, name='utilisation_of_services_list'),
    path('patient-registration/report/', patient_registration_report, name='patient_registration_report'),
    path('clinic-level-statistics/report/', clinic_level_statistics_list, name='clinic_level_statistics_list'),
    path('drug-dispensation/report/', drug_dispensation_stock_list, name='drug_dispensation_stock_list'),
    path('patient-adherence/report/', patient_adherence_list, name='patient_adherence_list'),
    path('village-profile/report/', village_profile_list, name='village_profile_list'),

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