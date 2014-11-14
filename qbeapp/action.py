# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav
"""

from qbeapp.dbs import *
import networkx as nx

SELECT = "SELECT"
FROM = "FROM"
WHERE = "WHERE"
ORDER_BY = "ORDER_BY"
SPACE = " "
COMMA = ", "
DOT = "."
INNER = "INNER"
LEFT_OUTER = "LEFT OUTER"
JOIN = "JOIN"
ON = "ON"

def join_on(kee, join_dict):
    return DOT.join([kee, join_dict.get(kee)])

def get_from_part(root, selected_tables):
    g = create_db_graph()
    join_tables = []
    for sel_table in selected_tables:
        join_tables = join_tables + nx.shortest_path(g, root, sel_table)
    join_subgraph = nx.subgraph(g, set(join_tables))
    joins = []
    joined_tables = []
    for edge in join_subgraph.edges():
        join_dict = g[edge[0]][edge[1]]['join'] 
        kees = join_dict.keys()
        on_val = ' = '.join((join_on(kees[0], join_dict), 
                             join_on(kees[1], join_dict)))
        inner_join_table = edge[0]
        if edge[0] in joined_tables or edge[0] == root:
            inner_join_table = edge[1]
        joined_tables.append(inner_join_table)
        joins.append(SPACE.join([INNER, JOIN, inner_join_table, ON, on_val]))
    joins_str = SPACE.join(joins)
    from_str = SPACE.join([root, joins_str]) 
    return from_str

def create_db_graph():
    g = nx.Graph()
    g.add_edge('auth_user', 'auth_user_groups', join={'auth_user':'id', 'auth_user_groups':'user_id'})
    g.add_edge('auth_group', 'auth_user_groups', join={'auth_group':'id', 'auth_user_groups':'group_id'})
    return g


def get_sidebar_tables():
    return get_tables()
    
def get_design_field_forms():  
    return get_table_clm_tuple()    
    
def get_report_from_data(report_for, report_data):
    query = generate_sql(report_for, report_data)
    print 'Query: ' + query
    return get_query_results(query)
        
def generate_sql(report_for, report_data):
    """
    Generates Select clause SQL String from submitted form data and
    returns the sql string
    """
    columns = COMMA.join(report_data)
    from_tbls = COMMA.join(get_tables_from_report_data(report_data))    
    return SPACE.join((SELECT, columns, FROM, 
                       get_from_part(report_for, 
                                     get_tables_from_report_data(report_data)))) #from_tbls))
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
