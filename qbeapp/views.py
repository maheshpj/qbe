# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: Mahesh.Jadhav
"""
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from qbeapp.forms import *
import qbeapp.utils as utils
import qbeapp.action as axn 
import logging
import csv

logger = logging.getLogger('qbe.log')
design_fields = []
TEMPLATE_INDEX = "qbeapp/index.html"

def index(request, template_name=TEMPLATE_INDEX):  
    """
    Displays the sidebar table tree and design fields view      
    """
    clear_design_fields()
    axn.init_qbe()
    ctx = {"tables": axn.get_sidebar_tables(), 
          "form": QbeForm(), 
          "design_fields": get_design_formset()}    
    return render_to_response(template_name, ctx)
    
def change_db(request, db_key, template_name=TEMPLATE_INDEX):
    axn.change_db(db_key)
    clear_design_fields()
    ctx = {"tables": axn.get_sidebar_tables(), 
          "form": QbeForm(), 
          "design_fields": get_design_formset()}    
    return render_to_response(template_name, ctx)

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
    ctx = {}
    if form.is_valid() and formset.is_valid():
        try:   
            report_data = get_report_data(formset)            
            report_for = form.cleaned_data['report_for']    
            report = axn.get_report_from_data(report_for, report_data)  
            header = axn.get_header(report_data)
        except:
            logger.exception("An error occurred")
        ctx = {"form": form, 
               "query": report['query'], 
               "header": header,
               "report": report['results']}    
    else:
        ctx = {"form": form, "qbeerrors": form.errors}
        logger.error('Invalid form: %s ', form.errors)
    return render_to_response(template_name, ctx)   
    
def get_report_data(formset):    
    report_data = []
    for f in formset.forms: 
        if is_valid_design_field(f.cleaned_data):
            logger.debug("Submitted report data: " + str(f.cleaned_data))
            report_data.append(f.cleaned_data)      
    return report_data    
         
def is_valid_design_field(design_field):
    """
    Checks if submitted field is valid or not and returns True/False
    """
    return design_field and design_field['field']

@csrf_exempt
def draw_graph(request):
    axn.draw_graph()
    return redirect('/')
    
@csrf_exempt
def export_csv(request):
    """    
    Create the HttpResponse object with the appropriate CSV header.
    returns response in csv format    
    """    
    response = HttpResponse(content_type='text/csv')    
    filename = "qbe-report" + str(utils.get_timestamp()) + ".csv"
    response['Content-Disposition'] = 'attachment;filename=' + filename
    logger.info('Exporting csv ' + filename)

    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST or None)
    report = None    
    if form.is_valid() and formset.is_valid():
        try:
            report_data = get_report_data(formset)
            if report_data:
                report_for = form.cleaned_data['report_for']    
                report = axn.get_report_from_data(report_for, report_data) 
                header = axn.get_header(report_data)
        except:
            logger.exception("An error occurred")
    if report:        
        writer = csv.writer(response)
        writer.writerow(header)
        for row in report['results']:
            writer.writerow(row)
    return response