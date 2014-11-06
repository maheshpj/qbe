from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from qbeapp.forms import *
from qbeapp.dbs import get_tables

design_fields = []

def index(request, template_name="qbeapp/index.html"):
    c =  {"tables": get_tables()}
    clear_design_fields()    
    return render_to_response(template_name, c)     
    
def get_aggregation():
    return ['avg', 'count', 'max', 'min', 'sum', 'group by']    
    
def add_design_column(request, table_name, column, template_name="qbeapp/index.html"):
    design_fields.append((table_name, column, None))
    return render_to_response(template_name, 
                              {"tables": get_tables(),
                                "total": get_aggregation(),
                                "design_fields": design_fields})
                                
def clear_design_fields():
    del design_fields[:]

@csrf_exempt   
def get_report(request, template_name="qbeapp/index.html"):
    c =  {"tables": get_tables(),
          "total": get_aggregation(),
            "design_fields": design_fields}
    print 'getting report...'
    form = QbeForm(request.POST or None)
    if form.is_valid():
        print 'form is valie'
        return HttpResponseRedirect("")
    return render_to_response(template_name, {'form': form})    
                                    

    
    
        