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

def convert_safe_text(content):
	try:
		if type(content) != str:
			content = str(content)
	except:
		content = str(content.encode("utf8"))
	return content


def send_mail(mail_to, mail_subject, mail_content, html_template = None,reply_to=None,cc=[],bcc =[],filepaths=None):
    ssl._create_default_https_context = ssl._create_unverified_context
    to_emails = [To(i,'') for i in mail_to]
    cc_emails = [Cc(i,'') for i in cc]
    bcc_emails = [Bcc(i,'') for i in bcc]

    if not html_template:
        html_message = mail_content
    else:
        template_name = html_template
        html_message = render_to_string(template_name,{'content':mail_content,'date':datetime.now().strftime("%d %B %Y")})
        html_message = convert_safe_text(html_message)
    message = Mail(from_email=settings.APP_EMAIL_SETTINGS['EMAIL_FROM'],
                   to_emails=to_emails,
                   subject=str(mail_subject),
                   html_content=html_message,
                   )
    if reply_to:
        message.reply_to = ReplyTo(reply_to)
    
    #Attaching the File in the Mail if Path is give with the Info
    # import ipdb;ipdb.set_trace()
    if filepaths:
        for file in filepaths:
            path = file.get("file_path")
            type  = file.get("file_type")
            name  = file.get("filename")
            with open(path, 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('{0}'.format(name)),
            FileType('application/{0}'.format(type)),
            Disposition('attachment')
            )
            message.add_attachment(attachedFile)
    if cc:
        message.add_cc(cc_emails)
    if bcc:
        message.add_bcc(bcc_emails)
    logger = logging.getLogger('user_obj')
    try:
        sg = SendGridAPIClient(settings.APP_EMAIL_SETTINGS['SENDGRID_API_KEY'])
        # sg.client.timeout = settings.APP_EMAIL_SETTINGS['SENDGRID_API_TIMEOUT']
        response_obj = sg.send(message)
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
