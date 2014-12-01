# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 2014

@author: Mahesh.Jadhav

This module will create a query from submitted user data
"""

from qbeapp.utils import *
import qbeapp.joins as jns
import logging
import re
import qbeapp.errors as errs
import qbeapp.utils as util

logger = logging.getLogger('qbe.log')
rgx = ',[\s]*|,|;[\s]*|;|[\s].*[aA][nN][dD].*\s'

def get_fields_from_report_data(report_data):
    """
    Returns list of fields like table.column 
    """
    fields = []
    for data in report_data:
        fields.append(data['field'])
    return fields

def get_included_fields(report_data):
    included_fields = []
    for data in report_data:
        if not data['exclude']:
            included_fields.append(data['field'])
    return included_fields

def get_query_columns(report_data):
    """
    Create and returns select columns in query
    """
    fields = get_included_fields(report_data)
    for data in report_data:
        if not data['exclude']:
            total = data['total']
            idx = fields.index(data['field'])
            if total and total != 'group by':
                total_field = total + parenthesized_str(data['field'])
                fields[idx] = total_field
    clms = COMMA.join(fields)
    return clms

def get_query_tables(report_data):
    """
    Returns set of tablenames from submitted report design fields data
    """
    fields = get_fields_from_report_data(report_data)
    return list(set(map(get_table_from_field, fields)))

def get_table_from_field(field):
    """
    Returns the tablename from submitted design field
    """
    return parse_table_clm_from_field(field)[0]
        
def parse_table_clm_from_field(field):
    return field.split(DOT)

def get_query_orderby(report_data):
    """
    Create and returns order by clause
    """
    sorts = []
    for data in report_data:
        if data['sort']:
            sorts.append(data['field'])
    order_by = COMMA.join(sorts)
    return order_by

def get_between(from_str):
    btwns = re.split(rgx, from_str)
    if len(btwns) == 2:
        return (SPACE + AND + SPACE).join([quote_str(x) for x in btwns])
    else:
        raise errs.QBEError("Invalid between criteria. Split values with comma or text 'and'")

def get_in(from_str):
    ins = re.split(rgx, from_str)
    return parenthesized_str(", ".join([quote_str(x) for x in ins]))

def create_criteria(data, cr):
    op = data['operator'] if cr == 'criteria' else data['oroperator']
    val = quote_str(data[cr])
    if op == 'between':
        val = get_between(data[cr])
    elif op == 'in':
        val = get_in(data[cr])
    return SPACE.join((data['field'], op, val))

def get_query_where(report_data):
    """
    Create and returns where clause
    """
    wheres, ors = [], []
    for data in report_data:
        if data['criteria']:
            wheres.append(create_criteria(data, 'criteria'))
        if data['orcriteria']:
            ors.append(create_criteria(data, 'orcriteria'))
    and_whr = AND.join(wheres)
    where = and_whr  
    if ors:
        or_whr = (SPACE + OR + SPACE).join(ors)    
        where = SPACE.join((and_whr, OR, or_whr)) 
    return where

def get_query_groupby(report_data):
    """
    Create and returns group by clause
    """
    grpbys = []
    for data in report_data:
        total = data['total']
        if total and total == 'group by':
                grpbys.append(data['field'])
    group_by = COMMA.join(grpbys)
    return group_by

def create_query_parts(columns, froms, **kwargs):
    query_parts = []
    query_parts.append(SELECT)
    query_parts.append(columns)
    query_parts.append(FROM)
    query_parts.append(froms)
    for k, v in kwargs.iteritems():
        query_parts.append(k)
        query_parts.append(str(v))
    return query_parts

def generate_sql(report_for, report_data):
    """
    Generates Select clause SQL String from submitted form data and
    returns the sql string
    """
    logger.info("Generating sql for " + report_for + "...")
    columns = get_query_columns(report_data)
    tables = get_query_tables(report_data)
    from_part = jns.get_from_part(report_for, tables)
    where = get_query_where(report_data)
    group_by = get_query_groupby(report_data)
    order_by = get_query_orderby(report_data)
    conditions = {}
    if where:
        conditions[WHERE] = where
    if group_by:
        conditions[GROUP_BY] = group_by
    if order_by:
        conditions[ORDER_BY] = order_by    
    query_parts = create_query_parts(columns, from_part, **conditions)
    query = SPACE.join(query_parts)
    return query