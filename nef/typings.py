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

BASIC_TYPE_DICT = {'int': int,
                   'str': str,
                   'bool': bool,
                   'float': float,
                   'List[int]': typing.List[int],
                   'List[str]': typing.List[str],
                   'List[bool]': typing.List[bool],
                   'List[float]': typing.List[float]}

BASIC_TYPE_DICT_REVERT = {int: 'int', float: 'float', bool: 'bool', str: 'str',
                          typing.List[int]: 'List[int]', typing.List[float]: 'List[float]',
                          typing.List[bool]: 'List[bool]', typing.List[str]: 'List[str]'}

BASIC_TYPE_CONVERTER = {int: int,
                        str: str,
                        bool: bool,
                        float: float,
                        typing.List[int]: lambda x: list(map(int, x[1:-1].split(','))),
                        typing.List[str]: lambda x: list(map(str, x[1:-1].split(','))),
                        typing.List[bool]: lambda x: list(map(bool, x[1:-1].split(','))),
                        typing.List[float]: lambda x: list(map(float, x[1:-1].split(',')))}
