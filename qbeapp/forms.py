# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:24:45 2014

@author: p7107498
"""

from django import forms
from qbeapp.dbs import get_table_names

def get_aggregation():
    return (('', ''), ('avg', 'avg'), ('count', 'count'), ('max', 'max'),
            ('min', 'min'), ('sum', 'sum'), ('group by', 'group by'))   

def report_for_mapping(table):
    return (table, table)
    
def report_for_choices():    
    return [('', 'Select report for...')] + map(report_for_mapping, get_table_names())
    
class DesignFieldForm(forms.Form):
    table_name = ""
    column_name = ""
    style_display = "none"
    field = forms.CharField(required=False, widget=forms.HiddenInput())
    show = forms.BooleanField(required=False)
    sort = forms.BooleanField(required=False)
    total = forms.ChoiceField(choices=get_aggregation(), required=False)
    criteria = forms.CharField(max_length=1000, required=False)
    orcriteria = forms.CharField(max_length=1000, required=False)
                                
class QbeForm(forms.Form):
    report_for = forms.ChoiceField(choices=report_for_choices(), required=True)  
    
    
 