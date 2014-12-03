# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav
"""

import qbeapp.dbs as db
import qbeapp.query as qry
import qbeapp.joins as grph
import logging
import qbeapp.charts as chrt
import qbeapp.errors as errs
import qbeapp.utils as utils
import numpy as np

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

def show_chart(report_for, report_data):
    try:    
        axis = chrt.get_axis_from_report_data(report_data)
        if not axis:
            raise errs.QBEError("Please provide X and Y axis to plot chart.")                  
        x_ax = axis['X']
        y_ax = axis['Y']
        
        report = get_report_from_data(report_for, report_data)  
        records = report['results']
        header = report['header']
        
        ax_data = chrt.get_chart_data(header, records, x_ax[0], y_ax[0])
        if not ax_data:
            raise errs.QBEError("No valid data found for plotting chart.")
    
        chrt.dyna_chart(report_for, 
                        x_ax[0].replace(utils.DOT, utils.APO_S), 
                        y_ax[0].replace(utils.DOT, utils.APO_S), 
                        x_ax, ax_data['X'], ax_data['Y'])
    except errs.QBEError:
        raise
    except:    
        raise errs.QBEError("Error occurred while processing bar chart")

def get_num_bins(size):
    num_bins = 50 if size > 500 else int(size/10)
    return num_bins

def get_mean(from_list):
    try:
        mean = np.mean(from_list)
    except TypeError as te:
        logger.debug("An error occurred: " + te.message)
        raise errs.QBEError("Input should be numeric")
    return mean 

def show_histogram(report_for, report_data):
    try:
        report = get_report_from_data(report_for, report_data)
        records = utils.reduceto_list(report['results'])
        if records:
            total = len(records)
            xlabel = report_data[0]['field']
            xlabel = xlabel.replace(utils.DOT, utils.APO_S)
            title = "Histogram of " + report_for
            sigma = 10
            mean = get_mean(records)
            num_bins = get_num_bins(total)
            
            logger.debug("Histogram value: ")
            logger.debug(" mu : " + str(mean))
            logger.debug(" sigma : " + str(sigma))
            logger.debug(" num_bins : " + str(num_bins))
            
            chrt.histogram(mean, sigma, records, num_bins, 
                           title, xlabel, 'Probability')
        else:
            raise errs.QBEError("No data found.")    
    except:
        raise             