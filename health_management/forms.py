from django import forms
from application_masters.models import *


class PhcForm(forms.ModelForm):
    code = forms.CharField(max_length=3, required=True)

    def __init__(self, *args, **kwargs):
        super(PhcForm, self).__init__(*args, **kwargs)
        self.fields['taluk'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=PHC
        fields=['name','code','taluk']

class SubcenterForm(forms.ModelForm):
    code = forms.CharField(max_length=3, required=True)

    def __init__(self, *args, **kwargs):
        super(SubcenterForm, self).__init__(*args, **kwargs)
        self.fields['phc'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=Subcenter
        fields=['name','code','phc']

class VillageForm(forms.ModelForm):
    code = forms.CharField(max_length=3, required=True)
    subcenter = forms.ModelChoiceField(queryset=Subcenter.objects.filter(status=2))

    def __init__(self, *args, **kwargs):
        super(VillageForm, self).__init__(*args, **kwargs)
        self.fields['subcenter'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=Village
        fields=['name','code','subcenter']
        

class MasterlookupForm(forms.ModelForm):
    class Meta:
        model=MasterLookup
        fields=['name']
    def save(self, commit=True):
        instance = super(MasterlookupForm, self).save(commit=False)
        instance.parent_id = 4 
        if commit:
            instance.save()
        return instance
    

        
    

medicine_type=[
    ('',''),
    ('Tab','Tab'),
    ('Syrup','Syrup'),
    ('Cap','Cap'),
    ('Powder','Powder'),
    ('Suspension','Suspension'),
    ('EyeDrop','EyeDrop'),
    ('Lotion','Lotion'),
    ('Inhaler','Inhaler'),
]
class MedicinesForm(forms.ModelForm):
    category_id = forms.CharField(
        max_length=3,
        label='category',
        widget=forms.Select(choices=[(cat.id,cat.name) for cat in Category.objects.filter(status=2,parent_id=0)]),
    )
    type = forms.CharField(
        widget=forms.Select(choices=medicine_type),
    )
    class Meta:
        model=Medicines
        fields=['name','code','type','category_id']


    # def __init__(self, *args, **kwargs):
    #     super(MedicinesForm, self).__init__(*args, **kwargs)
    #     self.fields['category_id'].fields.forms.Select = choices[(e.id, e.name) for e in Category.objects.all()]

        
