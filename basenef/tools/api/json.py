# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: json.py
@date: 4/9/2019
@desc:
'''
import json as json_

from .class_schema_parser import convert_class_to_schema, convert_schema_to_class
from .instance_dict_parser import convert_instance_to_dict, convert_dict_to_instance


def loads(json_string: str, *, schema = None):
    dct = json_.loads(json_string)
    checker = list(dct.keys())[0]
    if checker[0].islower():  # instance
        return convert_dict_to_instance(dct, schema = schema)
    else:
        return convert_schema_to_class(dct)


def load(path: str, *, schema = None):
    with open(path, 'r') as fin:
        dct = json_.load(fin)
    checker = list(dct.keys())[0]
    if checker[0].islower():  # instance
        return convert_dict_to_instance(dct, schema = schema)
    else:
        return convert_schema_to_class(dct)


def dumps(o, *, verbose = False):
    if not isinstance(o, list):
        o = [o]
    checker = isinstance(o[0], type)
    if not checker:  # instance
        dct = convert_instance_to_dict(o, verbose = verbose)
    else:
        dct = convert_class_to_schema(o, verbose = verbose)
    return json_.dumps(dct)


def dump(o: dict, path: str, *, verbose = False):
    if not isinstance(o, list):
        o = [o]
    checker = isinstance(o[0], type)
    if not checker:  # instance
        dct = convert_instance_to_dict(o, verbose = verbose)
    else:
        dct = convert_class_to_schema(o, verbose = verbose)
    with open(path, 'w') as fout:
        json_.dump(dct, fout, indent = 4, separators = [',', ':'])


from basenef.base import NefClass

NefClass.dumps = classmethod(lambda cls, verbose = False: dumps(cls, verbose = verbose))
