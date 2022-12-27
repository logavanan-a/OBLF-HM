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
    path('add/<model>/', master_add_form),
    path('edit/<model>/<id>/', master_edit_form),
    path('add/userprofile/', user_add),
    path('list/<model>/', master_list_form),
    path('edit/userprofile/<id>/', user_edit),
    path('<model>/<id>/delete/', delete_record,name='delete_record'),
	# path('mhu/push/<pk>/', Mhu_push.as_view()),

]