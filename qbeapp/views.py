from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from qbeapp.forms import *
from qbeapp.dbs import get_tables, get_table_clm_tuple
from django.forms.formsets import formset_factory

design_fields = []
TEMPLATE_INDEX = "qbeapp/index.html"

def index(request, template_name=TEMPLATE_INDEX):        
    clear_design_fields()
    c =  {"tables": get_tables(), 
          "form": QbeForm(), 
          "design_fields": get_design_formset()}
    
    return render_to_response(template_name, c)

def get_design_formset():                
    table_clm_tuples = get_table_clm_tuple()
    DesignFieldFormset = formset_factory(DesignFieldForm, 
                                         extra=len(table_clm_tuples))
    formset = DesignFieldFormset()
    count = 0    
    for form in formset:
        form.table_name = table_clm_tuples[count][0]
        form.column_name = table_clm_tuples[count][1]
        count = count + 1
    return formset    
                                
def clear_design_fields():
    del design_fields[:]

@csrf_exempt   
def get_report(request, template_name=TEMPLATE_INDEX):
    print 'getting report...'
    form = QbeForm(request.POST or None)
    DesignFieldFormset = formset_factory(DesignFieldForm)
    formset = DesignFieldFormset(request.POST, request.FILES)
    if form.is_valid():
        print 'form is valid'
    if formset.is_valid():
        print 'formset is valid'
    c =  {"tables": get_tables(), 
          "form": form, 
          "design_fields": formset}    
    return render_to_response(template_name, c)    
                                    

    
    
        