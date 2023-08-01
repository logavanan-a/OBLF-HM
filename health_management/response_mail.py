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
    py_c = patients.filter(server_created_on__date=prev_day)
    py_m = patients.filter(server_modified_on__date=prev_day).exclude(id__in=py_c.values_list('id', flat=True), server_created_on__in=py_c.values_list('server_created_on', flat=True))
    pcw_c = patients.filter(server_created_on__date__range=[current_week,prev_day])
    pcw_m = patients.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=pcw_c.values_list('id', flat=True), server_created_on__in=pcw_c.values_list('server_created_on', flat=True))
    pcm_c = patients.filter(server_created_on__date__range=[current_month,prev_day])
    pcm_m = patients.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=pcm_c.values_list('id', flat=True), server_created_on__in=pcm_c.values_list('server_created_on', flat=True))

    treatments = Treatments.objects.filter(status=2)
    ty_c = treatments.filter(server_created_on__date=prev_day)
    ty_m = treatments.filter(server_modified_on__date=prev_day).exclude(id__in=ty_c.values_list('id', flat=True), server_created_on__in=ty_c.values_list('server_created_on', flat=True))
    tcw_c = treatments.filter(server_created_on__date__range=[current_week,prev_day])
    tcw_m = treatments.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=tcw_c.values_list('id', flat=True), server_created_on__in=tcw_c.values_list('server_created_on', flat=True))
    tcm_c = treatments.filter(server_created_on__date__range=[current_month,prev_day])
    tcm_m = treatments.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=tcm_c.values_list('id', flat=True), server_created_on__in=tcm_c.values_list('server_created_on', flat=True))

    health = Health.objects.filter(status=2)
    hy_c = health.filter(server_created_on__date=prev_day)
    hy_m = health.filter(server_modified_on__date=prev_day).exclude(id__in=hy_c.values_list('id', flat=True), server_created_on__in=hy_c.values_list('server_created_on', flat=True))
    hcw_c = health.filter(server_created_on__date__range=[current_week,prev_day])
    hcw_m = health.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=hcw_c.values_list('id', flat=True), server_created_on__in=hcw_c.values_list('server_created_on', flat=True))
    hcm_c = health.filter(server_created_on__date__range=[current_month,prev_day])
    hcm_m = health.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=hcm_c.values_list('id', flat=True), server_created_on__in=hcm_c.values_list('server_created_on', flat=True))

    prescription = Prescription.objects.filter(status=2)
    pcy_c = prescription.filter(server_created_on__date=prev_day)
    pcy_m = prescription.filter(server_modified_on__date=prev_day).exclude(id__in=pcy_c.values_list('id', flat=True), server_created_on__in=pcy_c.values_list('server_created_on', flat=True))
    pccw_c = prescription.filter(server_created_on__date__range=[current_week,prev_day])
    pccw_m = prescription.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=pccw_c.values_list('id', flat=True), server_created_on__in=pccw_c.values_list('server_created_on', flat=True))
    pccm_c = prescription.filter(server_created_on__date__range=[current_month,prev_day])
    pccm_m = prescription.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=pccm_c.values_list('id', flat=True), server_created_on__in=pccm_c.values_list('server_created_on', flat=True))

    diagnosis = Diagnosis.objects.filter(status=2)
    dy_c = diagnosis.filter(server_created_on__date=prev_day)
    dy_m = diagnosis.filter(server_modified_on__date=prev_day).exclude(id__in=dy_c.values_list('id', flat=True), server_created_on__in=dy_c.values_list('server_created_on', flat=True))
    dcw_c = diagnosis.filter(server_created_on__date__range=[current_week,prev_day])
    dcw_m = diagnosis.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=dcw_c.values_list('id', flat=True), server_created_on__in=dcw_c.values_list('server_created_on', flat=True))
    dcm_c = diagnosis.filter(server_created_on__date__range=[current_month,prev_day])
    dcm_m = diagnosis.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=dcm_c.values_list('id', flat=True), server_created_on__in=dcm_c.values_list('server_created_on', flat=True))

    scanned_report = Scanned_Report.objects.filter(status=2)
    sry_c = scanned_report.filter(server_created_on__date=prev_day)
    sry_m = scanned_report.filter(server_modified_on__date=prev_day).exclude(id__in=sry_c.values_list('id', flat=True), server_created_on__in=sry_c.values_list('server_created_on', flat=True))
    srcw_c = scanned_report.filter(server_created_on__date__range=[current_week,prev_day])
    srcw_m = scanned_report.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=srcw_c.values_list('id', flat=True), server_created_on__in=srcw_c.values_list('server_created_on', flat=True))
    srcm_c = scanned_report.filter(server_created_on__date__range=[current_month,prev_day])
    srcm_m = scanned_report.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=srcm_c.values_list('id', flat=True), server_created_on__in=srcm_c.values_list('server_created_on', flat=True))

    home_visit = HomeVisit.objects.filter(status=2)
    hvy_c = home_visit.filter(server_created_on__date=prev_day)
    hvy_m = home_visit.filter(server_modified_on__date=prev_day).exclude(id__in=hvy_c.values_list('id', flat=True), server_created_on__in=hvy_c.values_list('server_created_on', flat=True))
    hvcw_c = home_visit.filter(server_created_on__date__range=[current_week,prev_day])
    hvcw_m = home_visit.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=hvcw_c.values_list('id', flat=True), server_created_on__in=hvcw_c.values_list('server_created_on', flat=True))
    hvcm_c = home_visit.filter(server_created_on__date__range=[current_month,prev_day])
    hvcm_m = home_visit.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=hvcm_c.values_list('id', flat=True), server_created_on__in=hvcm_c.values_list('server_created_on', flat=True))

    fee_payement = FeePayement.objects.filter(status=2)
    fpy_c = fee_payement.filter(server_created_on__date=prev_day)
    fpy_m = fee_payement.filter(server_modified_on__date=prev_day).exclude(id__in=fpy_c.values_list('id', flat=True), server_created_on__in=fpy_c.values_list('server_created_on', flat=True))
    fpcw_c = fee_payement.filter(server_created_on__date__range=[current_week,prev_day])
    fpcw_m = fee_payement.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=fpcw_c.values_list('id', flat=True), server_created_on__in=fpcw_c.values_list('server_created_on', flat=True))
    fpcm_c = fee_payement.filter(server_created_on__date__range=[current_month,prev_day])
    fpcm_m = fee_payement.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=fpcm_c.values_list('id', flat=True), server_created_on__in=fpcm_c.values_list('server_created_on', flat=True))
   
    form_column = [
    {"name":"Patient", "y_c": py_c.count(), "y_m": py_m.count(), "cw_c": pcw_c.count(), "cw_m": pcw_m.count(), "cm_c": pcm_c.count(), "cm_m": pcm_m.count(), "t": patients.count()},
    {"name":"Treatment", "y_c": ty_c.count(), "y_m": ty_m.count(), "cw_c": tcw_c.count(), "cw_m": tcw_m.count(), "cm_c": tcm_c.count(), "cm_m": tcm_m.count(), "t": treatments.count()},
    {"name":"Health", "y_c": hy_c.count(), "y_m": hy_m.count(), "cw_c": hcw_c.count(), "cw_m": hcw_m.count(), "cm_c": hcm_c.count(), "cm_m": hcm_m.count(), "t": health.count()},
    {"name":"Prescription", "y_c": pcy_c.count(), "y_m": pcy_m.count(), "cw_c": pccw_c.count(), "cw_m": pccw_m.count(), "cm_c": pccm_c.count(), "cm_m": pccm_m.count(), "t": prescription.count()},
    {"name":"Scanned Report", "y_c": sry_c.count(), "y_m": sry_m.count(), "cw_c": srcw_c.count(), "cw_m": srcw_m.count(), "cm_c": srcm_c.count(), "cm_m": srcm_m.count(), "t": scanned_report.count()},
    {"name":"Home Visit", "y_c": hvy_c.count(), "y_m": hvy_m.count(), "cw_c": hvcw_c.count(), "cw_m": hvcw_m.count(), "cm_c": hvcm_c.count(), "cm_m": hvcm_m.count(), "t": home_visit.count()},
    {"name":"Fee Payement", "y_c": fpy_c.count(), "y_m": fpy_m.count(), "cw_c": fpcw_c.count(), "cw_m": fpcw_m.count(), "cm_c": fpcm_c.count(), "cm_m": fpcm_m.count(), "t": fee_payement.count()},
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
    # send_mail(subject,message,"loga.vanan@thesocialbytes.com",to_,fail_silently=False,html_message=html_message)

    return send_data_obj


def attachment_email():
    from datetime import timedelta
    today = datetime.date.today()
    prev_day = today-timedelta(days=1)
    template_obj = MailTemplate.objects.get(template_name ="OBLF-HM Activity Mailer")
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