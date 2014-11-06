# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:24:45 2014

@author: p7107498
"""

from django import forms
from django.forms.formsets import formset_factory
from qbeapp.dbs import get_table_names

def get_aggregation():
    return ['avg', 'count', 'max', 'min', 'sum', 'group by']   
    
class DesignFieldForm(forms.Form):
    show = forms.BooleanField(required=False)
    sort = forms.BooleanField(required=False)
    total = forms.ChoiceField(widget=forms.Select, choices=get_aggregation(), 
                              required=False)
    criteria = forms.CharField(max_length=1000)
    orcriteria = forms.CharField(max_length=1000)
                                
class QbeForm(forms.Form):
    report_for = forms.ChoiceField(widget=forms.Select, 
                                   choices=get_table_names(), 
                                    required=True, help_text="Report for...")                                
    designFieldFormSet = formset_factory(DesignFieldForm, max_num=20)
    
 