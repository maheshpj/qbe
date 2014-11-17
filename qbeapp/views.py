# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: Mahesh.Jadhav
"""
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.forms.formsets import formset_factory
from qbeapp.forms import *
import qbeapp.action as axn 
import logging

logger = logging.getLogger('qbe.log')
design_fields = []
TEMPLATE_INDEX = "qbeapp/index.html"

def index(request, template_name=TEMPLATE_INDEX):  
    """
    Displays the sidebar table tree and design fields view      
    """
    clear_design_fields()
    c = {"tables": axn.get_sidebar_tables(), 
          "form": QbeForm(), 
          "design_fields": get_design_formset()}    
    return render_to_response(template_name, c)
    
def change_db(request, db_key, template_name=TEMPLATE_INDEX):
    axn.change_db(db_key)
    clear_design_fields()
    c = {"tables": axn.get_sidebar_tables(), 
          "form": QbeForm(), 
          "design_fields": get_design_formset()}    
    return render_to_response(template_name, c)

def get_design_formset():
    """
    Creates design field formset using columns available and returns formset    
    """                       
    design_field_forms = axn.get_design_field_forms()
    DesignFieldFormset = formset_factory(DesignFieldForm, 
                                         extra=len(design_field_forms))
    formset = create_formset_from_tables(DesignFieldFormset(), 
                                         design_field_forms)    
    return formset    

def create_formset_from_tables(formset, design_field_forms):
    count = 0 
    for form in formset:
        form.table_name = design_field_forms[count][0]
        form.column_name = design_field_forms[count][1]
        count = count + 1
    return  formset   
                            
def clear_design_fields():
    del design_fields[:]

@csrf_exempt   
def get_report(request, template_name=TEMPLATE_INDEX):
    """
    Creates the report from selected table columns and returns the report
    """
    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST or None)
    c = {}
    if form.is_valid() and formset.is_valid():
        report_data = []
        try:
            for f in formset.forms: 
                if is_valid_design_field(f.cleaned_data):
                    logger.debug("Submitted report data: " + str(f.cleaned_data))
                    report_data.append(f.cleaned_data)
            report_for = form.cleaned_data['report_for']    
            report = axn.get_report_from_data(report_for, report_data)
            header = axn.get_header(report_data)
            c = {"form": form, 
                 "query": report['query'], 
                 "header": header,
                 "report": report['results']}
        except:
            logger.exception("An error occurred")
    else:
        c = {"form": form, "qbeerrors": form.errors}
        logger.error('Invalid form: %s ', form.errors)
    return render_to_response(template_name, c)   
                                    
def is_valid_design_field(design_field):
    """
    Checks if submitted field is valid or not and returns True/False
    """
    return design_field and design_field['field']
        