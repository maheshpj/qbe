# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav
"""

from qbeapp.dbs import *


SELECT = "SELECT"
FROM = "FROM"
WHERE = "WHERE"
ORDER_BY = "ORDER_BY"
SPACE = " "
COMMA = ", "
DOT = "."

def get_sidebar_tables():
    return get_tables()
    
def get_design_field_forms():  
    return get_table_clm_tuple()    
    
def get_report_from_data(report_for, report_data):
    return get_query_results(generate_sql(report_for, report_data))
        
def generate_sql(report_for, report_data):
    """
    Generates Select clause SQL String from submitted form data and
    returns the sql string
    """
    columns = COMMA.join(report_data)
    from_tbls = COMMA.join(get_tables_from_report_data(report_data))    
    return SPACE.join((SELECT, columns, FROM, from_tbls))

def get_tables_from_report_data(report_data):
    """
    Returns set of tablenames from submitted report design fields data
    """
    return set(map(get_table_from_field, report_data))

def get_table_from_field(field):
    """
    Returns the tablename from submitted design field
    """
    return parse_table_clm_from_field(field)[0]
        
def parse_table_clm_from_field(field):
    return field.split(DOT)
