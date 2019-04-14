# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: instance_dict_parser.py
@date: 4/9/2019
@desc:
'''
from nef.typings import BASIC_TYPE_DICT_REVERT, BASIC_TYPE_CONVERTER


def _convert_single_instance_to_dict(obj: object = None, *, verbose = True):
    if obj is None:
        raise ValueError('valid instance are needed.')

    kwargs = {'classname': obj.__class__.__name__}
    for key, val in obj.fields():
        if not verbose and key.startswith('_'):
            continue
        if key == 'data':
            kwargs.update({'data': ''})
        elif val in BASIC_TYPE_DICT_REVERT:
            kwargs.update({key: getattr(obj, key)})
        else:
            kwargs.update(
                {key: _convert_single_instance_to_dict(getattr(obj, key), verbose = verbose)})

    return kwargs


def convert_instance_to_dict(objs: list, *, verbose = True):
    if objs is None:
        raise ValueError('valid instance are needed.')

    kwargs = {}
    for ind, obj in enumerate(objs):
        kwargs.update({str(ind): _convert_single_instance_to_dict(obj, verbose = verbose)})
    return kwargs


def convert_dict_to_instance(dct: dict, *, schema: dict):
    out = {}
    for key, val in dct.items():
        if 'classname' in val:
            classname = val['classname']
            if classname not in schema:
                raise ValueError(f'can not find valid class assigned for {key} in the first arg')
            cls = schema[classname]
            if isinstance(cls, dict):
                from .class_schema_parser import convert_schema_to_class
                cls = convert_schema_to_class(schema)[classname]
        else:
            raise ValueError(f"can not find valid classname in dct.['{key}']")

        kwargs = {}
        for field, type_ in cls.items(verbose = False):
            sub_ = val[field]
            if isinstance(sub_, dict):
                kwargs.update(
                    {field: convert_dict_to_instance({field: sub_}, schema = schema)[field]})
            else:
                kwargs.update({field: BASIC_TYPE_CONVERTER[type_](sub_)})
        out.update({key: cls(**kwargs)})
    return out
