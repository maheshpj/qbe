from django.shortcuts import render_to_response
from qbeapp.dbs import *

design_fields = []

def index(request):
    clear_design_fields()    
    return render_to_response("qbeapp/index.html", 
                              {"tables": get_tables()})     
    
def get_aggregation():
    return ['avg', 'count', 'max', 'min', 'sum', 'group by']    
    
def add_design_column(request, table_name, column):
    design_fields.append((table_name, column))
    return render_to_response("qbeapp/index.html", 
                              {"tables": get_tables(),
                                "total": get_aggregation(),
                                "design_fields": design_fields})
                                
def clear_design_fields():
    del design_fields[:]
                                    

    
    
        