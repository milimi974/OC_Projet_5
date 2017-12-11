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
    """ Format string with - """
    name = re.sub('[\']', '\\\'', name)
    return re.sub(r'\W+', ' ', name)


def clear_texte(texte):
    return json.dumps(texte)