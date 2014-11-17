# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav
"""

import qbeapp.dbs as db
import qbeapp.query as qry
import logging

logger = logging.getLogger('qbe.log')

def get_sidebar_tables():
    return db.get_tables()
    
def get_design_field_forms():  
    return db.get_table_clm_tuple()    

def get_report_from_data(report_for, report_data):    
    query = qry.generate_sql(report_for, report_data)
    results = db.get_query_results(query)
    return {'query': query, 'results': results}

def get_header(report_data):
    return qry.get_included_fields(report_data)
    
def change_db(db_key):
    db.manage_engine(db_key)    

