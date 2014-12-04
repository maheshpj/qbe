# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 15:30:08 2014

@author: Mahesh.Jadhav

This module uses networkx graphs to create database tables graph 
using foreign key as edge
"""
import logging

try:
    import networkx as nx
except ImportError:
    import sys
    print("NetworkX needed for graphs. Skipping")
    sys.exit(0)

from qbeapp.utils import *
import qbeapp.dbs as db
import qbeapp.errors as errs

logger = logging.getLogger('qbe.log')
graph = None
primary_key_dict = {}

def build_subgraph(g, root, selected_tables):
    """
    Builds subgraph from db graph using selected tables in design fields, uses 
    shortest path algorithm from root table to each table
    returns a subgraph
    """
    join_tables = []
    try:
        for sel_table in selected_tables:
            join_tables = join_tables + nx.shortest_path(g, root, sel_table)
    except:  
        raise errs.QBEError("Invalid table relations.")
    join_subgraph = nx.subgraph(g, set(join_tables + selected_tables))
    return join_subgraph


def joins_from_successors(join_subgraph, root):
    """
    Creates a dfs successors tree and use it to create joins with root
    returns all inner joins list
    Example:
       root = 'a'        
       successors = {'a': ['c'], 
                     'c': ['j', 'f'], 
                     'f': ['i'], 
                     'j': ['k']} 
                     
       from a
        inner join c on a.id = c.id
            inner join j on j.id = c.id
                inner join k on k.id = j.id
            inner join f on f.id = c.id
                inner join i on i.id = f.id         
    """    
    successors = nx.dfs_successors(join_subgraph, root)
    return create_joins(successors, root, [])

def create_joins(successors, key, joins):
    """
    Recurssive function to create inner joins using successors
    returns all inner joins list
    """
    vals = successors.get(key)
    if vals:
        for val in vals:
            joins.append(build_inner_join(key, val))
            create_joins(successors, val, joins)
    return joins             

def join_on(kee, join_dict):
    return DOT.join([kee, join_dict.get(kee)]) 
    
def build_inner_join(source, target):
    try:
        join_dict = get_db_graph()[source][target].get('fk')
    except:
        raise errs.QBEError("Invalid nodes.")       
    kees = join_dict.keys()
    pk_tbl = source    
    if (pk_tbl == kees[0]):
        pk_tbl = target    
    pk_dict = get_db_pk_dict()         
    on_val = ' = '.join((join_on(kees[0], join_dict), 
                         DOT.join([pk_tbl, pk_dict.get(pk_tbl)])))
    inner_join_str = SPACE.join([INNER, JOIN, target, ON, on_val])    
    return inner_join_str
    
def get_from_part(root, selected_tables):
    """
    Creates a from join statements using selected tables and root table
    return string of from joins
    """
    join_subgraph = build_subgraph(get_db_graph(), root, selected_tables)
    joins = joins_from_successors(join_subgraph, root) 
    joins_str = SPACE.join(joins)
    from_str = SPACE.join([root, joins_str]) 
    return from_str

def get_db_graph():
    return graph

def get_db_pk_dict():
    return primary_key_dict

def create_primary_key_dict():    
    """
    Creates table and its primary key relation dictionary like 
        {'tablename': 'pk_column'}
    returns dictionary
    """
    logger.info("Creating primary key dict...")
    global primary_key_dict
    if not primary_key_dict:
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
    Creates database graph using edge like 
        {'pk_table', 'fk_table', fk={'fk_table': 'fk_column'}}
    returns networkx graph object
    """
    logger.info("Creating database graph...")
    global graph
    if not graph:
        graph = nx.Graph()
        for tbl in db.get_sorted_tbls():
            for clm in tbl.columns:
                for fk in clm.foreign_keys:
                    graph.add_edge(str(fk.column.table), str(clm.table), 
                                   fk={str(clm.table): str(clm.name)})
    return graph
