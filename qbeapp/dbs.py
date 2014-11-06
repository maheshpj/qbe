# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: p7107498
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection

engine = create_engine('sqlite:///I:/Project/qbe/db.sqlite3')
insp = reflection.Inspector.from_engine(engine)

def get_table_names():
    return insp.get_table_names()
    
def get_column_names(table_name, schema=None):
    return insp.get_columns(table_name, schema)
        
def get_table_clms(table_name):
    return (table_name, get_column_names(table_name))
    
def get_tables():
    return dict(map(get_table_clms, get_table_names()))