from application_masters.models import *
import base64
from dateutil.relativedelta import relativedelta
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from health_management.models import *

register = template.Library()

# @register.simple_tag
# def disply_indicator_values(res_id, ind_id, keys):
#     mission_response = MissionIndicatorAchievement.objects.get(id = res_id)
#     return mission_response.response.get(keys + str(ind_id))