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

    path('village-of-drugs/list/', village_of_drugs_list, name='village_of_drug_list'),
    path('add/village-of-drugs/', add_village_of_drugs, name='add_village_of_drugs'),

    path('drug-dispensation/list/', drug_dispensation_stock_list, name='drug_dispensation_stock_list'),
    path('add/medicine/', add_medicine_stock, name='add_medicine_stock'),

    path('medicine/list/', medicine_stock_list, name='medicine_stock_list'),

    path('add/userprofile/', user_add),
    path('edit/userprofile/<id>/', user_edit),
    path('list/<model>/', master_list_form),
    path('add/<model>/', master_add_form),
    path('edit/<model>/<id>/', master_edit_form),
    path('<model>/<id>/delete/', delete_record,name='delete_record'),
	# path('mhu/push/<pk>/', Mhu_push.as_view()),

]