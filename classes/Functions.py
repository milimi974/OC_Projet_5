#!/_env/bin/python
# coding: utf-8

# accented_string is of type 'unicode'
import unidecode
import re


def serialized_title(name):
    """ Format string with - """
    a = unidecode.unidecode(str(name)).lower().replace(' ', '-')
    return re.sub('[^A-Za-z0-9 \-]+', '', a)