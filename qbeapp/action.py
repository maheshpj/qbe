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

def create_subgraph(g, root, selected_tables):
    join_tables = []
    for sel_table in selected_tables:
        join_tables = join_tables + nx.shortest_path(g, root, sel_table)
    join_subgraph = nx.subgraph(g, set(join_tables))
    return join_subgraph

def get_from_part(root, selected_tables):
    g = create_db_graph()
    pk_dict = create_primary_key_dict()
    join_subgraph = create_subgraph(g, root, selected_tables)
    joins = []
    joined_tables = []
    for edge in join_subgraph.edges():
        join_dict = g[edge[0]][edge[1]]['fk'] 
        kees = join_dict.keys()
        pk_tbl = edge[0]      
        if edge[0] == kees[0]:
            pk_tbl = edge[1]            
        on_val = ' = '.join((join_on(kees[0], join_dict), 
                             DOT.join([pk_tbl, pk_dict[pk_tbl]])))
        inner_join_table = edge[0]
        if edge[0] in joined_tables or edge[0] == root:
            inner_join_table = edge[1]
        joined_tables.append(inner_join_table)
        joins.append(SPACE.join([INNER, JOIN, inner_join_table, ON, on_val]))
    joins_str = SPACE.join(joins)
    from_str = SPACE.join([root, joins_str]) 
    return from_str

def create_primary_key_dict():    
    """
    Creates table and its primary key relation dictionary like {'tablename': 'pk_column'}
    returns dictionary
    """
    primary_key_dict = {}
    for t in get_sorted_tbls():
        for pk in t.primary_key:
            pk = str(pk)
            if DOT in pk:
                tbl_pk = pk.split(DOT)
                primary_key_dict[tbl_pk[0]] = tbl_pk[1]
    return primary_key_dict
    
def create_db_graph():
    """
    Creates database graph using edge like {'pk_table', 'fk_table', fk={'fk_table': 'fk_column'}}
    returns networkx graph object
    """
    graph = nx.Graph()
    for tbl in get_sorted_tbls():
        for clm in tbl.columns:
            for fk in clm.foreign_keys:
                graph.add_edge(str(fk.column.table), str(clm.table), 
                               fk={str(clm.table): str(clm.name)})
    return graph


def get_sidebar_tables():
    return get_tables()
    
def get_design_field_forms():  
    return get_table_clm_tuple()    
        
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
    
def get_report_from_data(report_for, report_data):    
    query = generate_sql(report_for, report_data)
    results = get_query_results(query)
    return {'query': query, 'results': results}
