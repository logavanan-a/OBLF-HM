from django import forms
from application_masters.models import *


class PhcForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+','placeholder': 'Enter Name'}))
    code = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z0-9 ]+','placeholder': 'Enter Code'}))

    def __init__(self, *args, **kwargs):
        super(PhcForm, self).__init__(*args, **kwargs)
        self.fields['taluk'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=PHC
        fields=['name','code','taluk']

class SubcenterForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+','placeholder': 'Enter Name'}))
    code = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z0-9 ]+','placeholder': 'Enter Code'}))

    def __init__(self, *args, **kwargs):
        super(SubcenterForm, self).__init__(*args, **kwargs)
        self.fields['phc'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=Subcenter
        fields=['name','code','phc']

class VillageForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+','placeholder': 'Enter Name'}))
    code = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z0-9 ]+','placeholder': 'Enter Code'}))
    subcenter = forms.ModelChoiceField(queryset=Subcenter.objects.filter(status=2),empty_label="Select Subcenter")

    def __init__(self, *args, **kwargs):
        super(VillageForm, self).__init__(*args, **kwargs)
        self.fields['subcenter'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=Village
        fields=['name','code','subcenter']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+','placeholder': 'Enter Name'}))

    class Meta:
        model=Category
        fields=['name']

class MasterlookupForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'pattern':'[A-Za-z ]+','placeholder': 'Enter Name'}))
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
    ('','--------'),
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
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Name'}))
    medicines_type = forms.CharField(
        widget=forms.Select(choices=medicine_type),
    )
    medicine_id = forms.CharField(required=False, label='Generation', widget=forms.TextInput(attrs={'pattern':'[0-9]+','placeholder': 'Enter Medicine Name'}))

    def __init__(self, *args, **kwargs):
        super(MedicinesForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['medicines_type'].widget.attrs['class'] = 'form-select'

    class Meta:
        model=Medicines
        fields=['name', 'medicines_type', 'category', 'medicine_id']

#  widget=forms.TextInput(attrs={'pattern':'[A-Za-z0-9 ]+'})
    # def __init__(self, *args, **kwargs):
    #     super(MedicinesForm, self).__init__(*args, **kwargs)
    #     self.fields['category_id'].fields.forms.Select = choices[(e.id, e.name) for e in Category.objects.all()]

        
