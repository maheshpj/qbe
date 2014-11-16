# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:24:45 2014

@author: Mahesh.Jadhav

This module contains the qbe form and design fields formset classes
"""

from django import forms
from qbeapp.dbs import get_table_names
import qbeapp.utils as utils

def report_for_mapping(table):
    return (table, table)
    
def report_choices():   
    """
    Creates choices to display in Report for drop down 
    and return list of choices
    """
    return [('', 'Select report for...')] + map(report_for_mapping, get_table_names())
    
class DesignFieldForm(forms.Form):
    """
    Design field form
    """
    table_name = ""
    column_name = ""
    style_display = "none"
    field = forms.CharField(required=False, widget=forms.HiddenInput())
    exclude = forms.BooleanField(required=False)
    sort = forms.BooleanField(required=False)
    total = forms.ChoiceField(choices=utils.AGGREGATION, required=False)
    criteria = forms.CharField(max_length=1000, required=False)
    orcriteria = forms.CharField(max_length=1000, required=False)
                                
class QbeForm(forms.Form):
    report_for = forms.ChoiceField(choices=report_choices(), required=True)