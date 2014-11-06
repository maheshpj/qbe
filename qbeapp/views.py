from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from qbeapp.dbs import *
from django.views.decorators.csrf import csrf_exempt

design_fields = []

def index(request):
    c =  {"tables": get_tables()}
    clear_design_fields()    
    return render_to_response("qbeapp/index.html", c)     
    
def get_aggregation():
    return ['avg', 'count', 'max', 'min', 'sum', 'group by']    
    
def add_design_column(request, table_name, column):
    design_fields.append((table_name, column, None))
    return render_to_response("qbeapp/index.html", 
                              {"tables": get_tables(),
                                "total": get_aggregation(),
                                "design_fields": design_fields})
                                
def clear_design_fields():
    del design_fields[:]

@csrf_exempt   
def get_report(request):
    c =  {"tables": get_tables(),
          "total": get_aggregation(),
            "design_fields": design_fields}
    if request.method == 'POST':    
        print 'getting report...'
        print request.POST
        return HttpResponseRedirect("")
    return render_to_response("qbeapp/index.html", c)    
                                    

    
    
        