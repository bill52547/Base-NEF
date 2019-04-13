# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: nef
@file: typings.py
@date: 4/13/2019
@desc:
'''
import typing

BASIC_TYPES = [int, str, bool, float, typing.List[int], typing.List[str], typing.List[bool],
               typing.List[float]]

BASIC_TYPE_DICT = {'int': (int, lambda x: int(x)),
                   'str': (str, lambda x: str(x)),
                   'bool': (bool, lambda x: bool(x)),
                   'float': (float, lambda x: float(x)),
                   'List[int]': (typing.List[int], lambda x: map(int, x)),
                   'List[str]': (typing.List[str], lambda x: map(str, x)),
                   'List[bool]': (typing.List[bool], lambda x: map(bool, x)),
                   'List[float]': (typing.List[float], lambda x: map(float, x))}
