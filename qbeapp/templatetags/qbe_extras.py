from django import template
import sqlalchemy

register = template.Library()

@register.filter(name='class_name')
def class_name(value):
    return value.__class__.__name__

@register.filter(name='convert_datatype')
def convert_datatype(saType):
    type = "Unknown"
    if isinstance(saType,sqlalchemy.types.INTEGER):
        type = "Integer"
    elif isinstance(saType,sqlalchemy.types.VARCHAR):
        type = "String"
    elif isinstance(saType,sqlalchemy.types.DATE):
        type = "Date"
    elif isinstance(saType,sqlalchemy.types.BOOLEAN):
        type = "Boolean"
    
    """
    elif isinstance(saType,sqlalchemy.dialects.mysql.base._FloatType):
        type = "Double"
    """
    return type

