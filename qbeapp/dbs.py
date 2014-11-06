# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: p7107498
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from django.conf import settings

engine = create_engine('sqlite:///' + settings.DATABASES['default']['NAME'])
insp = reflection.Inspector.from_engine(engine)

def get_table_names():
    return insp.get_table_names()
    
def get_column_names(table_name, schema=None):
    return insp.get_columns(table_name, schema)
        
def get_table_clms(table_name):
    return (table_name, get_column_names(table_name))
    
def get_tables():
    return dict(map(get_table_clms, get_table_names()))
    
def get_table_clm_tuple():
    tables = get_tables()
    tables_tuple = []
    for k in tables.keys():
        for v in tables[k]:
            tables_tuple.append((k, v['name']))
    return tables_tuple