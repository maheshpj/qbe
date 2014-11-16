# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav

This module uses networkx graphs to create database tables graph using foreign key as edge
"""

from qbeapp.utils import *
import qbeapp.dbs as db
import networkx as nx
import logging

logger = logging.getLogger('qbe.log')

def join_on(kee, join_dict):
    return DOT.join([kee, join_dict.get(kee)])

def create_subgraph(g, root, selected_tables):
    """
    Creates a subgraph from db graph using selected tables in design fields, uses 
    shortest path algorithm from root table to each table
    returns a subgraph
    """
    join_tables = []
    for sel_table in selected_tables:
        join_tables = join_tables + nx.shortest_path(g, root, sel_table)
    join_subgraph = nx.subgraph(g, set(join_tables))
    return join_subgraph

def get_from_part(root, selected_tables):
    """
    Creates a from join statements using selected tables and root table
    return string of from joins
    """
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
    for t in db.get_sorted_tbls():
        for pk in t.primary_key:
            pk = str(pk)
            if DOT in pk:
                tbl_pk = pk.split(DOT)
                primary_key_dict[tbl_pk[0]] = tbl_pk[1]
            else:
                logger.debug("No Primary Key column:" + pk)
    return primary_key_dict
    
def create_db_graph():
    """
    Creates database graph using edge like {'pk_table', 'fk_table', fk={'fk_table': 'fk_column'}}
    returns networkx graph object
    """
    logger.info("Creating database graph...")
    graph = nx.Graph()
    for tbl in db.get_sorted_tbls():
        for clm in tbl.columns:
            for fk in clm.foreign_keys:
                graph.add_edge(str(fk.column.table), str(clm.table), 
                               fk={str(clm.table): str(clm.name)})
    return graph

