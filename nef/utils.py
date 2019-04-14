# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: nef
@file: utils.py
@date: 4/14/2019
@desc:
'''

import sys
import tqdm as tqdm_


def is_notebook():
    '''check if the current environment is `ipython`/ `notebook`
    '''
    return 'ipykernel' in sys.modules


def tqdm(*args, **kwargs):
    '''same as tqdm.tqdm
    Automatically switch between `tqdm.tqdm` and `tqdm.tqdm_notebook` accoding to the runtime
    environment.
    '''
    if is_notebook():
        return tqdm_.tqdm_notebook(*args, **kwargs)
    else:
        return tqdm_.tqdm(*args, **kwargs)


def any_type_loader(path_: str):
    import numpy as np
    from scipy import sparse
    if path_.endswith('npy'):
        return np.load(path_)
    elif path_.endswith('npz'):
        return sparse.load_npz(path_)
    else:
        raise NotImplementedError(f'`any_type_loader` does not {path_} loading. ')
