# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 13:39:44 2014

@author: Mahesh.Jadhav

This module uses Sqlalchemy library to fetch database metadata from various 
databases and also executes the auto generate sql statement to fetch records
"""
try:
    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.engine import reflection
    from sqlalchemy.sql import text
    from sqlalchemy.engine.url import URL
except ImportError:
    import sys
    print("sqlalchemy needed for database communication. Skipping")
    sys.exit(0)
from django.conf import settings
import qbeapp.utils as utils
import logging
import qbeapp.errors as errs

logger = logging.getLogger('qbe.log')
engine = None
insp = None

table_dict = {}
sorted_tbls = []

def get_db_dict(db='default'):
    return settings.DATABASES[db]
    
def get_drivername_from_engine(engine):
    return utils.DATABASE_ENGINES.get(engine, "Driver name not found.") 

def manage_engine(db_key='default'):
    db = get_db_dict(db_key)
    database_url = URL(get_drivername_from_engine(db['ENGINE']),
                       username=db['USER'], 
                       password=db['PASSWORD'], 
                       host=db['HOST'], 
                       port=db['PORT'],
                       database=db['NAME'])
    global engine, insp                   
    engine = create_engine(database_url)
    insp = reflection.Inspector.from_engine(engine)

manage_engine()

def get_sorted_tbls(eng=engine):
    global sorted_tbls
    if not sorted_tbls:
        logger.info('Getting sorted tables...')
        sorted_tbls = get_db_metadata(eng).sorted_tables
    return sorted_tbls

def get_db_metadata(eng=engine):
    metadata = MetaData(eng)
    metadata.reflect(bind=eng)
    return metadata

def get_table_names(schema=None, order_by=None):
    return insp.get_table_names(schema, order_by)
    
def get_column_names(table_name, schema=None):
    return insp.get_columns(table_name, schema)
        
def get_table_clms(table_name, schema=None):
    """
    Returns the tuple of tablename and its columns
    """
    return (table_name, get_column_names(table_name, schema))
    
def get_tables(schema=None, order_by=None):
    """
    Fetches the database metadata for tablename and its columns 
    returns the dictionary having tablename as key and its columns as value
    """
    global table_dict
    if not table_dict:
        table_dict = dict(map(get_table_clms, 
                              get_table_names(schema, order_by)))    
    return table_dict
    
def get_table_clm_tuple():
    """
    Returns table and its columns as tuples
    """
    tables = get_tables()
    tables_tuple = []
    for table_name, columns in tables.iteritems():
        for column in columns:
            tables_tuple.append((table_name, column['name']))
    return tables_tuple

def get_query_results(sqlstr):    
    return execute_sql(create_sql_from_sqlstr(sqlstr))
    
def create_sql_from_sqlstr(sqlstr): 
    """
    Create and returns the sqlalchemy text sql using provided sql string
    """
    logger.debug("QBE Query: " + sqlstr)
    return text(sqlstr)
    
def execute_sql(sql):
    """
    Execute the sql and returns the records
    """
    connection = engine.connect()
    try:
        results = connection.execute(sql).fetchall() 
    except:
        raise errs.QBEError("Error while executing query. Invalid query.")
    finally:
        connection.close()
    return results    