# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: Mahesh.Jadhav
"""
from django.shortcuts import render_to_response, redirect
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

def create_formset_from_tables(formset, design_field_forms):
    count = 0 
    for form in formset:
        dsn_field = design_field_forms[count]
        form.table_name = dsn_field[0]
        form.column_name = dsn_field[1]['name']
        form.datatype = dsn_field[1]['type']
        count = count + 1
    return  formset   

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
    try:
        ctx = process_form(request)

        if not ctx.get('qbeerrors'):
            report_for = ctx['report_for']
            report_data = ctx['report_data']

            report = axn.get_report_from_data(report_for, report_data)  
            records = paginate_report(report['results'], page)
            ctx = { "query": report['query'], 
                    "header": report['header'],
                    "report": records
                    }
    except errs.QBEError as err:
        logger.exception("An error occurred: " + err.value)
        ctx = {"qbeerrors": err.value}  
    except:
        raise       

    return render_to_response(template_name, ctx) 

def draw_graph(request, template_name=TEMPLATE_INDEX):
    try:        
        axn.draw_graph()
    except errs.QBEError as err:
        logger.exception("An error occurred: " + err.value)
        ctx = {"qbeerrors": err.value}  
        return render_to_response(template_name, ctx) 
    except:
        raise

    return redirect('/')

def show_report_chart(request, template_name=TEMPLATE_INDEX):
    try:
        ctx = process_form(request)

        if not ctx.get('qbeerrors'):
            report_for = ctx['report_for']
            report_data = ctx['report_data']
            axn.show_chart(report_for, report_data)
        else:
            return render_to_response(template_name, ctx)
    except errs.QBEError as err:
        logger.exception("An error occurred: " + err.value)
        ctx = {"qbeerrors": err.value}  
        return render_to_response(template_name, ctx)  
    except:
        raise  

    return redirect('/')  

def filter_report_for_hist(report_data, hist_id):
    for data in report_data:
        if data["field"] == hist_id:
            return [data]
    return None        
    
def show_histogram(request, hist_id, template_name=TEMPLATE_INDEX):
    try:
        ctx = process_form(request)

        if not ctx.get('qbeerrors'):
            report_for = ctx['report_for']
            report_data = ctx['report_data']
            hist_data = filter_report_for_hist(report_data, hist_id)
            if hist_data:                
                axn.show_histogram(report_for, hist_data)
            else:
                raise errs.QBEError("No valid data found for histogram.")
        else:
            return render_to_response(template_name, ctx)
    except errs.QBEError as err:
        logger.exception("An error occurred: " + err.value)
        ctx = {"qbeerrors": err.value}  
        return render_to_response(template_name, ctx)  
    except:
        raise  

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

    try:
        ctx = process_form(request)

        if not ctx.get('qbeerrors'):
            report_for = ctx['report_for']
            report_data = ctx['report_data']

            report = axn.get_report_from_data(report_for, report_data)             
            if report:        
                writer = csv.writer(response)
                writer.writerow(report['header'])
                for row in report['results']:
                    writer.writerow(row)
        else:
            return render_to_response(template_name, ctx)
    except errs.QBEError as err:
        logger.exception("An error occurred: " + err.value)
        ctx = {"qbeerrors": err.value}  
        return render_to_response(template_name, ctx)  
    except:
        raise 

    return response
    
def get_report_data(formset):    
    report_data = []
    for f in formset.forms: 
        if (is_valid_design_field(f.cleaned_data)):
            logger.debug("Submitted report data: " + str(f.cleaned_data))
            report_data.append(f.cleaned_data)      
    return report_data    
         
def is_valid_design_field(design_field):
    """
    Checks if submitted field is valid or not and returns True/False
    """
    return design_field and design_field['field']

def get_custom_field_map(form_data):
    field = utils.DOT.join([form_data.get('table_name'), 
                            form_data.get('column_name')
            ])
    form_data['field'] = field
    form_data['custom'] = True
    return form_data

def process_form(request):
    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST or None)

    if form.is_valid() and formset.is_valid():
        report_data = get_report_data(formset)
        form_data = form.cleaned_data
        if (form_data['table_name'] and form_data['column_name']):
            custom_field_map = get_custom_field_map(form_data)
            report_data.append(custom_field_map)
        report_for = form_data['report_for']  
        if (report_data and report_for):                
            return {"report_for": report_for, "report_data": report_data}
        else:
            return {"qbeerrors": "Input data is not valid."}                       
    else:        
        logger.error('Invalid form: %s ', form.errors)
        return {"form": form, "qbeerrors": form.errors}