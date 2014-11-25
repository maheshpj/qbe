# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav
"""

import qbeapp.dbs as db
import qbeapp.query as qry
import qbeapp.joins as grph
import logging

logger = logging.getLogger('qbe.log')

def get_sidebar_tables():
    return db.get_tables()
    
def get_design_field_forms():  
    return db.get_table_clm_tuple()    

def get_report_from_data(report_for, report_data):    
    query = qry.generate_sql(report_for, report_data)
    results = db.get_query_results(query)
    header = get_header(report_data)
    return {'query': query, 'results': results, 'header': header}

def get_header(report_data):
    return qry.get_included_fields(report_data)
    
def change_db(db_key):
    db.manage_engine(db_key)  
    
def init_qbe():
    grph.create_db_graph()
    grph.create_primary_key_dict()      

def draw_graph():
    grph.draw_graph(grph.get_db_graph())

