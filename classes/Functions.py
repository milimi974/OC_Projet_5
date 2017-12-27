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


def clear_texte(text):
    """ escape special char """
    if type(text) == str:
        text = json.dumps(text)
        text = text[1:]
        text = text[:-1]

    return text


def clear_varchar(text):
    """ escape ' """
    # remove special char
    text = re.sub('r"[^a-zA-Z %., 0-9€_\-()@áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\'\"]"g', "", str(text))
    # remove extra space
    text = re.sub('r"\s+"g', " ", text)
    # remove "
    text = re.sub('r"[\"]"g', "'", text)
    # escape '
    text = re.sub('r"[\']"g', "\\'", text)
    return text


def decode_varchar(text):
    """ escape ' """
    return re.sub('r"[\\ ]"g', "'", str(text))


def decode_text(text):
    """ decode encoding text with clear_text"""

    if type(text) == str:
        text = '\"{}\"'.format(text)
        return json.loads(text)
    return text


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
                return clear_varchar(value)
            elif type_name == "text":
                return decode_text(value)
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
                if type(value) == list:
                    return [int(el) for el in value]
                return int(value)
            elif type_name == "varchar":
                if type(value) == list:
                    return [decode_varchar(el).strip() for el in value]
                return decode_varchar(value).strip()
            elif type_name == "text":
                if type(value) == list:
                    return [clear_texte(el) for el in value]
                return clear_texte(value)
            elif type_name == "url":
                if type(value) == list:
                    return [str(el).strip() for el in value]
                return value.strip()
            elif type_name == "serialized":
                if type(value) == list:
                    return [serialized_title(el).strip() for el in value]
                return serialized_title(value).strip()
            elif type_name == "datetime":
                if type(value) == list:
                    return [str(el) for el in value]
                return str(value)

    return value
