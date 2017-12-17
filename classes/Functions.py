#!/_env/bin/python
# coding: utf-8

# accented_string is of type 'unicode'
import unidecode
import re
import json


def serialized_title(name):
    """ Format string with - """
    a = re.sub(' +', ' ', str(name))
    a = unidecode.unidecode(a).lower().replace(' ', '-')
    return re.sub('[^A-Za-z0-9 \-]+', '', a)


def clear_title(name):
    """ Format string remove special char """
    return re.sub(r'\W+', ' ', name)


def clear_texte(texte):
    """ escape special char """
    if type(texte) == str:
        return json.dumps(texte)
    return texte


def decode_texte(texte):
    """ decode encoding text with clear_text"""
    if type(texte) == str:
        return str(json.loads(texte))
    return texte


def decode_field(format_fields, field, value):
    """ remove format field value
    Keyword arguments:
    field -- str
    value -- ??

    """

    if not format_fields == "":
        if field in format_fields:
            type_name = format_fields[field]
            if type_name == "primary":
                return int(value)
            elif type_name == "varchar":
                return value
            elif type_name == "text":
                return decode_texte(value)
            elif type_name == "url":
                return value
            elif type_name == "serialized":
                return value
            elif type_name == "datetime":
                return value

    return value


def parse_field(format_fields, field, value):
    """ format field value
    Keyword arguments:
    field -- str
    value -- ??

    """

    if not format_fields == "":
        if field in format_fields:
            type_name = format_fields[field]
            if type_name == "primary":
                return int(value)
            elif type_name == "varchar":
                return clear_title(value).strip()
            elif type_name == "text":
                return clear_texte(value)
            elif type_name == "url":
                return value.strip()
            elif type_name == "serialized":
                return serialized_title(value).strip()
            elif type_name == "datetime":
                return str(value)

    return value
