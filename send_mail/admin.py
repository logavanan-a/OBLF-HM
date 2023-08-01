from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.unregister(MailTemplate)

@admin.register(MailTemplate)
class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_name','description','subject','content','created_by','html_template', 'status']
    fields = ['created_by','template_name','description','subject','content','html_template', 'status']
    # list_filter = ('created_by',)

    # SS

# admin.site.unregister(MailData)

@admin.register(MailData)
class MailDataAdmin(admin.ModelAdmin):
    list_display = ['template_name','subject','content', 'created_by', 'status']
    #fields = ['template_name','subject','content','created_by', 'status']

#     def is_active(self, obj):
#         return obj.active == 2 
#     is_active.boolean = True