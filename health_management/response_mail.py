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
    py_m = [pt.id for pt in patients.filter(server_modified_on__date=prev_day) if pt.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != pt.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    pcw_c = patients.filter(server_created_on__date__range=[current_week,prev_day])
    pcw_m = [pt.id for pt in patients.filter(server_modified_on__date__range=[current_week,prev_day]) if pt.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != pt.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    pcm_c = patients.filter(server_created_on__date__range=[current_month,prev_day])
    pcm_m = [pt.id for pt in patients.filter(server_modified_on__date__range=[current_month,prev_day]) if pt.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != pt.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]

    treatments = Treatments.objects.filter(status=2, patient_uuid__in=patients.values_list('uuid', flat=True))
    ty_c = treatments.filter(server_created_on__date=prev_day)
    ty_m = [tm.id for tm in treatments.filter(server_modified_on__date=prev_day) if tm.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != tm.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    tcw_c = treatments.filter(server_created_on__date__range=[current_week,prev_day])
    tcw_m = [tm.id for tm in treatments.filter(server_modified_on__date__range=[current_week,prev_day]) if tm.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != tm.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    tcm_c = treatments.filter(server_created_on__date__range=[current_month,prev_day])
    tcm_m = [tm.id for tm in treatments.filter(server_modified_on__date__range=[current_month,prev_day]) if tm.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != tm.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]

    health = Health.objects.filter(status=2, patient_uuid__in=patients.values_list('uuid', flat=True))
    hy_c = health.filter(server_created_on__date=prev_day)
    hy_m = [hc.id for hc in health.filter(server_modified_on__date=prev_day) if hc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != hc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    hcw_c = health.filter(server_created_on__date__range=[current_week,prev_day])
    hcw_m = [hc.id for hc in health.filter(server_modified_on__date__range=[current_week,prev_day]) if hc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != hc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    hcm_c = health.filter(server_created_on__date__range=[current_month,prev_day])
    hcm_m = [hc.id for hc in health.filter(server_modified_on__date__range=[current_month,prev_day]) if hc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != hc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]

    prescription = Prescription.objects.filter(status=2, treatment_uuid__in=treatments.values_list('uuid', flat=True))
    pcy_c = prescription.filter(server_created_on__date=prev_day)
    pcy_m = [pc.id for pc in prescription.filter(server_modified_on__date=prev_day) if pc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != pc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    pccw_c = prescription.filter(server_created_on__date__range=[current_week,prev_day])
    pccw_m = [pc.id for pc in prescription.filter(server_modified_on__date__range=[current_week,prev_day]) if pc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != pc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    pccm_c = prescription.filter(server_created_on__date__range=[current_month,prev_day])
    pccm_m = [pc.id for pc in prescription.filter(server_modified_on__date__range=[current_month,prev_day]) if pc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != pc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]

    diagnosis = Diagnosis.objects.filter(status=2)
    dy_c = diagnosis.filter(server_created_on__date=prev_day)
    dy_m = diagnosis.filter(server_modified_on__date=prev_day).exclude(id__in=dy_c.values_list('id', flat=True), server_modified_on__date__in=dy_c.values_list('server_created_on__date', flat=True), server_modified_on__hour__in=dy_c.values_list('server_created_on__hour', flat=True), server_modified_on__minute__in=dy_c.values_list('server_created_on__minute', flat=True))
    dcw_c = diagnosis.filter(server_created_on__date__range=[current_week,prev_day])
    dcw_m = diagnosis.filter(server_modified_on__date__range=[current_week,prev_day]).exclude(id__in=dcw_c.values_list('id', flat=True), server_modified_on__date__in=dcw_c.values_list('server_created_on__date', flat=True), server_modified_on__hour__in=dcw_c.values_list('server_created_on__hour', flat=True), server_modified_on__minute__in=dcw_c.values_list('server_created_on__minute', flat=True))
    dcm_c = diagnosis.filter(server_created_on__date__range=[current_month,prev_day])
    dcm_m = diagnosis.filter(server_modified_on__date__range=[current_month,prev_day]).exclude(id__in=dcm_c.values_list('id', flat=True), server_modified_on__date__in=dcm_c.values_list('server_created_on__date', flat=True), server_modified_on__hour__in=dcm_c.values_list('server_created_on__hour', flat=True), server_modified_on__minute__in=dcm_c.values_list('server_created_on__minute', flat=True))


    scanned_report = Scanned_Report.objects.filter(status=2,patient_uuid__in=patients.values_list('uuid', flat=True))
    sry_c = scanned_report.filter(server_created_on__date=prev_day)
    sry_m = [sc.id for sc in scanned_report.filter(server_modified_on__date=prev_day) if sc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != sc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    srcw_c = scanned_report.filter(server_created_on__date__range=[current_week,prev_day])
    srcw_m = [sc.id for sc in scanned_report.filter(server_modified_on__date__range=[current_week,prev_day]) if sc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != sc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    srcm_c = scanned_report.filter(server_created_on__date__range=[current_month,prev_day])
    srcm_m = [sc.id for sc in scanned_report.filter(server_modified_on__date__range=[current_month,prev_day]) if sc.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != sc.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]

    home_visit = HomeVisit.objects.filter(status=2,patient_uuid__in=patients.values_list('uuid', flat=True))
    hvy_c = home_visit.filter(server_created_on__date=prev_day)
    hvy_m = [fv.id for fv in home_visit.filter(server_modified_on__date=prev_day) if fv.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != fv.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    hvcw_c = home_visit.filter(server_created_on__date__range=[current_week,prev_day])
    hvcw_m = [fv.id for fv in home_visit.filter(server_modified_on__date__range=[current_week,prev_day]) if fv.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != fv.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    hvcm_c = home_visit.filter(server_created_on__date__range=[current_month,prev_day])
    hvcm_m = [fv.id for fv in home_visit.filter(server_modified_on__date__range=[current_month,prev_day]) if fv.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != fv.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]


    fee_payement = FeePayement.objects.filter(status=2,patient_uuid__in=patients.values_list('uuid', flat=True))
    fpy_c = fee_payement.filter(server_created_on__date=prev_day)
    fpy_m = [fp.id for fp in fee_payement.filter(server_modified_on__date=prev_day) if fp.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != fp.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    fpcw_c = fee_payement.filter(server_created_on__date__range=[current_week,prev_day])
    fpcw_m = [fp.id for fp in fee_payement.filter(server_modified_on__date__range=[current_month,prev_day]) if fp.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != fp.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
    fpcm_c = fee_payement.filter(server_created_on__date__range=[current_month,prev_day])
    fpcm_m = [fp.id for fp in fee_payement.filter(server_modified_on__date__range=[current_month,prev_day]) if fp.server_created_on.strftime("%Y-%m-%d %H:%M:%S") != fp.server_modified_on.strftime("%Y-%m-%d %H:%M:%S")]
   
    form_column = [
    {"name":"Patient", "y_c": py_c.count(), "y_m": len(py_m), "cw_c": pcw_c.count(), "cw_m": len(pcw_m), "cm_c": pcm_c.count(), "cm_m": len(pcm_m), "t": patients.count()},
    {"name":"Treatment", "y_c": ty_c.count(), "y_m": len(ty_m), "cw_c": tcw_c.count(), "cw_m": len(tcw_m), "cm_c": tcm_c.count(), "cm_m": len(tcm_m), "t": treatments.count()},
    {"name":"Health", "y_c": hy_c.count(), "y_m": len(hy_m), "cw_c": hcw_c.count(), "cw_m": len(hcw_m), "cm_c": hcm_c.count(), "cm_m": len(hcm_m), "t": health.count()},
    {"name":"Prescription", "y_c": pcy_c.count(), "y_m": len(pcy_m), "cw_c": pccw_c.count(), "cw_m": len(pccw_m), "cm_c": pccm_c.count(), "cm_m": len(pccm_m), "t": prescription.count()},
    {"name":"Scanned Report", "y_c": sry_c.count(), "y_m": len(sry_m), "cw_c": srcw_c.count(), "cw_m": len(srcw_m), "cm_c": srcm_c.count(), "cm_m": len(srcm_m), "t": scanned_report.count()},
    {"name":"Home Visit", "y_c": hvy_c.count(), "y_m": len(hvy_m), "cw_c": hvcw_c.count(), "cw_m": len(hvcw_m), "cm_c": hvcm_c.count(), "cm_m": len(hvcm_m), "t": home_visit.count()},
    {"name":"Fee Payement", "y_c": fpy_c.count(), "y_m": len(fpy_m), "cw_c": fpcw_c.count(), "cw_m": len(fpcw_m), "cm_c": fpcm_c.count(), "cm_m": len(fpcm_m), "t": fee_payement.count()},
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
    content = content.replace("@@date",str(prev_day))
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