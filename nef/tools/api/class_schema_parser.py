# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: class_schema_parser.py
@date: 4/8/2019
@desc:
'''

import numpy as np

from nef.base import make_nef_class
from nef.typings import BASIC_TYPES, BASIC_TYPE_DICT_REVERT, BASIC_TYPE_DICT


def _to_string(o):
    if isinstance(o, np.ndarray):
        return np.array2string(o, separator = ',')
    else:
        return str(o)


def _convert_single_class_to_schema(cls: type, verbose = True):
    kwargs = {}
    out = {}
    for key, val in cls.fields():
        if not verbose and key.startswith('_'):
            continue
        elif key == 'data':
            kwargs.update({key: ['Url']})
        elif val in BASIC_TYPES:
            kwargs.update({key: BASIC_TYPE_DICT_REVERT[val]})
        else:
            out.update(_convert_single_class_to_schema(val, verbose = verbose))
            kwargs.update({key: val.__name__})

    out.update({cls.__name__: kwargs})
    return out


def convert_class_to_schema(class_list: list = None, verbose = True):
    if class_list is None:
        return {}

    dct = {}

    for cls in class_list:
        class_name = cls.__name__
        if class_name in dct:
            pass
        else:
            dct.update(_convert_single_class_to_schema(cls, verbose = verbose))
    return dct


def convert_schema_to_class(dct: dict):
    out = {}
    for key, val in dct.items():
        fields = {}
        for k, v in val.items():
            if v in BASIC_TYPE_DICT:
                type_ = BASIC_TYPE_DICT[v]
            elif v in out:
                type_ = out[v]
            fields.update({k: type_})

        cls = make_nef_class(key, fields)
        out.update({key: cls})
    return out
