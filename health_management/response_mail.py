from OBLH_HM.settings import ACTIVITY_MAIL_RECIEVER, ACTIVITY_MAIL_CC
from health_management.models import *
from django.template import loader
from django.core.mail import send_mail
from send_mail.models import *
from django.db.models import Count
# import datetime



def survey_responses():
    from datetime import timedelta
    today = datetime.date.today()
    prev_day = today-timedelta(days=1)
    current_week = prev_day - datetime.timedelta(days=prev_day.weekday())
    current_month = datetime.date.today().replace(day=1)
    patients = Patients.objects.filter(status=2)
    py_c = patients.filter(server_created_on__date=prev_day).count()
    py_m = patients.filter(server_modified_on__date=prev_day).count()
    pcw_c = patients.filter(server_created_on__date__range=[current_week,prev_day]).count()
    pcw_m = patients.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    pcm_c = patients.filter(server_created_on__date__range=[current_month,prev_day]).count()
    pcm_m = patients.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    treatments = Treatments.objects.filter(status=2)
    ty_c = treatments.filter(server_created_on__date=prev_day).count()
    ty_m = treatments.filter(server_modified_on__date=prev_day).count()
    tcw_c = treatments.filter(server_created_on__date__range=[current_week,prev_day]).count()
    tcw_m = treatments.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    tcm_c = treatments.filter(server_created_on__date__range=[current_month,prev_day]).count()
    tcm_m = treatments.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    health = Health.objects.filter(status=2)
    hy_c = health.filter(server_created_on__date=prev_day).count()
    hy_m = health.filter(server_modified_on__date=prev_day).count()
    hcw_c = health.filter(server_created_on__date__range=[current_week,prev_day]).count()
    hcw_m = health.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    hcm_c = health.filter(server_created_on__date__range=[current_month,prev_day]).count()
    hcm_m = health.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    prescription = Prescription.objects.filter(status=2)
    pcy_c = prescription.filter(server_created_on__date=prev_day).count()
    pcy_m = prescription.filter(server_modified_on__date=prev_day).count()
    pccw_c = prescription.filter(server_created_on__date__range=[current_week,prev_day]).count()
    pccw_m = prescription.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    pccm_c = prescription.filter(server_created_on__date__range=[current_month,prev_day]).count()
    pccm_m = prescription.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    diagnosis = Diagnosis.objects.filter(status=2)
    dy_c = diagnosis.filter(server_created_on__date=prev_day).count()
    dy_m = diagnosis.filter(server_modified_on__date=prev_day).count()
    dcw_c = diagnosis.filter(server_created_on__date__range=[current_week,prev_day]).count()
    dcw_m = diagnosis.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    dcm_c = diagnosis.filter(server_created_on__date__range=[current_month,prev_day]).count()
    dcm_m = diagnosis.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    scanned_report = Scanned_Report.objects.filter(status=2)
    sry_c = scanned_report.filter(server_created_on__date=prev_day).count()
    sry_m = scanned_report.filter(server_modified_on__date=prev_day).count()
    srcw_c = scanned_report.filter(server_created_on__date__range=[current_week,prev_day]).count()
    srcw_m = scanned_report.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    srcm_c = scanned_report.filter(server_created_on__date__range=[current_month,prev_day]).count()
    srcm_m = scanned_report.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    home_visit = HomeVisit.objects.filter(status=2)
    hvy_c = home_visit.filter(server_created_on__date=prev_day).count()
    hvy_m = home_visit.filter(server_modified_on__date=prev_day).count()
    hvcw_c = home_visit.filter(server_created_on__date__range=[current_week,prev_day]).count()
    hvcw_m = home_visit.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    hvcm_c = home_visit.filter(server_created_on__date__range=[current_month,prev_day]).count()
    hvcm_m = home_visit.filter(server_modified_on__date__range=[current_month,prev_day]).count()

    fee_payement = FeePayement.objects.filter(status=2)
    fpy_c = fee_payement.filter(server_created_on__date=prev_day).count()
    fpy_m = fee_payement.filter(server_modified_on__date=prev_day).count()
    fpcw_c = fee_payement.filter(server_created_on__date__range=[current_week,prev_day]).count()
    fpcw_m = fee_payement.filter(server_modified_on__date__range=[current_week,prev_day]).count()
    fpcm_c = fee_payement.filter(server_created_on__date__range=[current_month,prev_day]).count()
    fpcm_m = fee_payement.filter(server_modified_on__date__range=[current_month,prev_day]).count()
   
    form_column = [
    {"name":"Patient", "y_c": py_c, "y_m": py_m, "cw_c": pcw_c, "cw_m": pcw_m, "cm_c": pcm_c, "cm_m": pcm_m, "t": patients.count()},
    {"name":"Treatment", "y_c": ty_c, "y_m": ty_m, "cw_c": tcw_c, "cw_m": tcw_m, "cm_c": tcm_c, "cm_m": tcm_m, "t": treatments.count()},
    {"name":"Health", "y_c": hy_c, "y_m": hy_m, "cw_c": hcw_c, "cw_m": hcw_m, "cm_c": hcm_c, "cm_m": hcm_m, "t": health.count()},
    {"name":"Prescription", "y_c": pcy_c, "y_m": pcy_m, "cw_c": pccw_c, "cw_m": pccw_m, "cm_c": pccm_c, "cm_m": pccm_m, "t": prescription.count()},
    {"name":"Scanned Report", "y_c": sry_c, "y_m": sry_m, "cw_c": srcw_c, "cw_m": srcw_m, "cm_c": srcm_c, "cm_m": srcm_m, "t": scanned_report.count()},
    {"name":"Home Visit", "y_c": hvy_c, "y_m": hvy_m, "cw_c": hvcw_c, "cw_m": hvcw_m, "cm_c": hvcm_c, "cm_m": hvcm_m, "t": home_visit.count()},
    {"name":"Fee Payement", "y_c": fpy_c, "y_m": fpy_m, "cw_c": fpcw_c, "cw_m": fpcw_m, "cm_c": fpcm_c, "cm_m": fpcm_m, "t": fee_payement.count()},
    ]

        

    template_obj = MailTemplate.objects.get(template_name ="OBLF-HM Activity Mailer")
    send_to_cc = ''
    send_to_bcc = ''
    subject = template_obj.subject +' - '+ today.strftime("%d/%m/%Y")
    content = template_obj.content
    dynamic_content = ""
    for form  in form_column:
        survey_name = form["name"]
        yes_response_created = form["y_c"]
        yes_response_modified = form["y_m"]
        current_week_response_created = form["cw_c"]
        current_week_response_modified = form["cw_m"]
        current_month_response_created = form["cm_c"]
        current_month_response_modified = form["cm_m"]
        total_response   = form["t"]

        dynamic_content = dynamic_content + "<tr>  <td>{0}</td> <td>{1}</td>  <td>{2}</td> <td>{3}</td> <td>{4}</td> <td>{5}</td> <td>{6}</td> <td>{7}</td> <tr>".format(survey_name , yes_response_created,yes_response_modified,current_week_response_created,current_week_response_modified,current_month_response_created,current_month_response_modified,total_response)
    content = content.replace("@@tbody",dynamic_content)
    # # to_ = ["girish.n.s@mahiti.org","pervin.d@mahiti.org","dmresearch@akrspi.org"]
    to_ = ';'.join(ACTIVITY_MAIL_RECIEVER)
    send_to_cc = ';'.join(ACTIVITY_MAIL_CC)
    send_data_obj = MailData.objects.create(subject = subject,content = content,mail_to = to_,
                                        mail_cc =send_to_cc,mail_bcc =send_to_bcc,priority = 1,mail_status = 1, 
                                        template_name = template_obj )
    # send_mail(subject,message,"mis@akrspi.org",to_,fail_silently=False,html_message=html_message)

    return send_data_obj


def attachment_email():
    from datetime import timedelta
    today = datetime.date.today()
    prev_day = today-timedelta(days=1)
    template_obj = MailTemplate.objects.get(template_name ="House Hold Activity Mailer")
    send_to_cc = ''
    send_to_bcc = ''
    subject = template_obj.subject
    content = template_obj.content
    content = content.replace("@@date",str(previous_day))
    # to_ = ["girish.n.s@mahiti.org","pervin.d@mahiti.org","dmresearch@akrspi.org"]
    to_ = ';'.join(ACTIVITY_MAIL_RECIEVER)
    send_to_cc = ';'.join(ACTIVITY_MAIL_CC)
    send_data_obj = MailData.objects.create(subject = subject,content = content,mail_to = to_,
                                        mail_cc =send_to_cc,mail_bcc =send_to_bcc,priority = 1,mail_status = 1, 
                                        template_name = template_obj )
  

    send_data_obj.file_paths.append({"filename":"HouseHoldActivity.csv","file_path":"media/export_data/data_dump_survey_425_2021Sep02235336.xlsx","file_type":"csv"})
    send_data_obj.save()
    # send_mail(subject,message,"mis@akrspi.org",to_,fail_silently=False,html_message=html_message)

    return send_data_obj