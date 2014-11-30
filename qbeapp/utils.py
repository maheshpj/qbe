# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 2014

@author: Mahesh.Jadhav

"""

import time
import datetime
import itertools

SELECT = "SELECT"
FROM = "FROM"
WHERE = "WHERE"
GROUP_BY = "GROUP BY"
ORDER_BY = "ORDER BY"
SPACE = " "
COMMA = ", "
DOT = "."
INNER = "INNER"
LEFT_OUTER = "LEFT OUTER"
JOIN = "JOIN"
ON = "ON"
AND = "AND"
OR = "OR"
APO_S = "'s "

AGGREGATION = (('', ''), ('avg', 'avg'), ('count', 'count'), ('max', 'max'), 
               ('min', 'min'), ('sum', 'sum'), ('upper', 'upper'), 
               ('lower', 'lower'), ('group by', 'group by'))
OPERATORS = (('=', '='), ('>=', '>='), ('<=', '<='), ('>', '>'), ('<', '<'), 
             ('<>', '<>'), ('like', 'like'), ('between', 'between'), 
             ('in', 'in'))
CHART = (('', 'Axis...'), ('X', 'X'), ('Y', 'Y'))
             
DATABASE_ENGINES = {
        'django.db.backends.postgresql_psycopg2': 'postgresql+psycopg2',
        'django.db.backends.postgresql': 'postgresql',
        'django.db.backends.mysql': 'mysql',
        'django.db.backends.mssql': 'mssql',
        'django.db.backends.sqlite3': 'sqlite',
        'django.db.backends.oracle': 'oracle',
        }              

def quote_str(str):
    return "'" + str + "'"

def parenthesized_str(str):
    return "(" + str + ")"
    
def get_timestamp():
    ts = time.time()
    t_format = '%Y-%m-%d_%H-%M-%S'
    return datetime.datetime.fromtimestamp(ts).strftime(t_format)    

def reduceto_list(from_list):
    """ 
    Reduces a list of lists into a single list
    
    example:
    t = [(18,), (19,), (10,)]
    list(itertools.chain(*t))
    [18, 19, 10]
    """
    return list(itertools.chain(*from_list))