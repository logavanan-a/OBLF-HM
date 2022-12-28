from django import forms
from application_masters.models import *


class PhcForm(forms.ModelForm):
    class Meta:
        model=PHC
        fields=['name','code','taluk']

class SubcenterForm(forms.ModelForm):
    class Meta:
        model=Subcenter
        fields=['name','code','phc']

class VillageForm(forms.ModelForm):
    class Meta:
        model=Village
        fields=['name','code','subcenter']

medicine_type=[
    ('',''),
    ('Tab','Tab'),
    ('Syrup','Syrup'),
    ('Tube','Tube'),
    ('Each','Each'),
    ('Cap','Cap'),
    ('Suspension','Suspension'),
    ('Drop','Drop'),
    ('Emulsion','Emulsion'),
    ('Powder','Powder'),
    ('Liquid','Liquid'),
    ('Lotion','Lotion'),
    ('Inhaler','Inhaler')
]
class MedicinesForm(forms.ModelForm):
    category = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=[(cat.id,cat.name) for cat in Category.objects.filter(status=2,parent_id=0)]),
    )
    type = forms.CharField(
        widget=forms.Select(choices=medicine_type),
    )
    class Meta:
        model=Medicines
        fields=['name','code','type','category']
        
