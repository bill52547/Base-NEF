# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: nef
@file: io.py
@date: 4/14/2019
@desc:
'''

import numpy as np
from scipy import sparse


def any_type_loader(path_: str):
    if path_.endswith('npy'):
        return np.load(path_)
    elif path_.endswith('npz'):
        return sparse.load_npz(path_)
    else:
        raise NotImplementedError(f'`any_type_loader` does not {path_} loading. ')
