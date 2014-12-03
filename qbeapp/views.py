# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: Mahesh.Jadhav
"""
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from qbeapp.forms import *
import qbeapp.utils as utils
import qbeapp.action as axn 
import logging
import csv
import qbeapp.errors as errs

logger = logging.getLogger('qbe.log')
design_fields = []
TEMPLATE_INDEX = "qbeapp/index.html"
PAGE_RECORDS = 25

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
        dsn_field = design_field_forms[count]
        form.table_name = dsn_field[0]
        form.column_name = dsn_field[1]['name']
        form.datatype = dsn_field[1]['type']
        count = count + 1
    return  formset   
                            
def clear_design_fields():
    del design_fields[:]

def paginate_report(report, page):
    paginator = Paginator(report, PAGE_RECORDS) 
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)
    return records    
       
def get_report(request, page=None, template_name=TEMPLATE_INDEX):
    """
    Creates the report from selected table columns and returns the report
    also paginate the report records
    """
    logger.debug("Requested page: " + str(page))
    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST or None)
    ctx = {}
    if form.is_valid() and formset.is_valid():
        try:   
            report_data = get_report_data(formset)            
            report_for = form.cleaned_data['report_for']  
            if report_data and report_for:                  
                report = axn.get_report_from_data(report_for, report_data)  
                records = paginate_report(report['results'], page)
                ctx = {"form": form, 
                       "query": report['query'], 
                       "header": report['header'],
                       "report": records}
            else:
                raise errs.QBEError("No valid data found for report.")
        except errs.QBEError as err:
            logger.exception("An error occurred: " + err.value)
            ctx = {"qbeerrors": err.value}    
    else:
        ctx = {"form": form, "qbeerrors": form.errors}
        logger.error('Invalid form: %s ', form.errors)
    ctx.update(csrf(request))    
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

def draw_graph(request):
    axn.draw_graph()
    return redirect('/')

def show_report_chart(request, template_name=TEMPLATE_INDEX):
    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST or None)
    ctx = {}
    if form.is_valid() and formset.is_valid():
        try:   
            report_data = get_report_data(formset)            
            report_for = form.cleaned_data['report_for']  
            if report_data and report_for:                
                axn.show_chart(report_for, report_data)
            else:
                raise errs.QBEError("No valid data found for report chart.")
        except errs.QBEError as err:
            logger.exception("An error occurred: " + err.value)
            ctx = {"qbeerrors": err.value}                
            return render_to_response(template_name, ctx) 
    else:
        ctx = {"form": form, "qbeerrors": form.errors}
        logger.error('Invalid form: %s ', form.errors)
        return render_to_response(template_name, ctx)
    return redirect('/')  

def filter_report_for_hist(report_data, hist_id):
    for data in report_data:
        if data["field"] == hist_id:
            return [data]
    return None        
    
def show_histogram(request, hist_id, template_name=TEMPLATE_INDEX):
    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST or None)
    ctx = {}
    if form.is_valid() and formset.is_valid():
        try:   
            report_data = get_report_data(formset)        
            hist_data = filter_report_for_hist(report_data, hist_id)
            report_for = form.cleaned_data['report_for']  
            if hist_data and report_for:                
                axn.show_histogram(report_for, hist_data)
            else:
                raise errs.QBEError("No valid data found for histogram.")
        except errs.QBEError as err:
            logger.exception("An error occurred: " + err.value)
            ctx = {"qbeerrors": err.value}                
            return render_to_response(template_name, ctx) 
    else:
        ctx = {"form": form, "qbeerrors": form.errors}
        logger.error('Invalid form: %s ', form.errors)
        return render_to_response(template_name, ctx)
    return redirect('/')  
    
def export_csv(request, template_name=TEMPLATE_INDEX):
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
            report_for = form.cleaned_data['report_for']  
            if report_data and report_for:  
                report = axn.get_report_from_data(report_for, report_data) 
            else:
                raise errs.QBEError("No valid data found for report.")
        except errs.QBEError as err:
            logger.exception("An error occurred: " + err.value)
            ctx = {"qbeerrors": err.value}
            return render_to_response(template_name, ctx) 
        except:
            logger.exception("An error occurred")
    if report:        
        writer = csv.writer(response)
        writer.writerow(report['header'])
        for row in report['results']:
            writer.writerow(row)
    return response
