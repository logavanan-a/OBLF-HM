from django.contrib import admin
from django.urls import path
from application_masters.views import *

app_name = "sql_queries"

urlpatterns = [
    path('', login_view, name="login"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('learning/sql_listing/', sql_learning, name="/learning/sql_listing/"),
]