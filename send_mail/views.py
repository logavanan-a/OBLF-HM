from __future__ import unicode_literals
from django.shortcuts import render
from .models import *
# Create your views here.
from django.template.loader import render_to_string
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import To, Mail,ReplyTo,Email,Cc,Bcc,Attachment, FileContent, FileName, FileType, Disposition, to_email
from string import Template
import logging
from django.conf import settings
import os
from datetime import datetime
import sys, traceback
import base64
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def convert_safe_text(content):
	try:
		if type(content) != str:
			content = str(content)
	except:
		content = str(content.encode("utf8"))
	return content


def send_mail(mail_to, mail_subject, mail_content, html_template = None,reply_to=None,cc=[],bcc =[],filepaths=None):
    if not html_template:
        html_message = mail_content
    else:
        template_name = html_template
        html_string = render_to_string(template_name,{'content':mail_content,'date':datetime.now().strftime("%d %B %Y")})
        html_message = convert_safe_text(html_string)
    msg = MIMEMultipart()
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = ", ".join(mail_to)
    msg['Subject'] = str(mail_subject)
    isTls = True
    part = MIMEText(html_message, 'html')
    msg.attach(part)
    logger = logging.getLogger('user_obj')
    try:
        smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        if isTls:
            smtp.starttls()
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        msg_send_status = smtp.sendmail(msg['From'], mail_to, msg.as_string())
        smtp.quit()
        response = {'status':200,'message':'success'}
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_stack = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        message = str(error_stack)
        logger.error(message)
        #e.body will display details of the error from sendgrid
        logger.error(e.body)
        response = {'status':500,'message':'failed-'+message}
    return response