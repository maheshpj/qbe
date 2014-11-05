from django.shortcuts import render_to_response
import datetime
from sqlalchemy import *
from sqlalchemy.engine import reflection

engine = create_engine('sqlite:///D:/Mahesh/Projects/qbe/db.sqlite3')
insp = reflection.Inspector.from_engine(engine)
design_fields = []

def index(request):
    design_fields = []    
    return render_to_response("qbeapp/index.html", 
                              {"tables": get_tables(),
                               "total": get_aggregation()})
    
def cur_datetime():
    return datetime.datetime.now()
    
def get_table_names():
    return insp.get_table_names()
    
def get_column_names(table_name, schema=None):
    return insp.get_columns(table_name, schema)
        
def get_table_clms(table_name):
    return (table_name, get_column_names(table_name))
    
def get_tables():
    return dict(map(get_table_clms, get_table_names()))
    
def get_aggregation():
    return ['avg', 'count', 'max', 'min', 'sum', 'group by']    
    
def add_design_column(request, table_name, column):
    design_fields.append((table_name, column))
    return render_to_response("qbeapp/index.html", 
                              {"tables": get_tables(),
                                "total": get_aggregation(),
                                "design_fields": design_fields})
    
    
        