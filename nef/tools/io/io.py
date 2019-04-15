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
import os
from nef.utils import separator

DATABASE_PATH = os.environ['HOME'] + separator + 'Database_nef' + separator
RESOURCE_PATH = DATABASE_PATH + 'resources' + separator
SCHEMA_PATH = DATABASE_PATH + 'schemas' + separator
CACHE_PATH = DATABASE_PATH + 'caches' + separator
LOG_PATH = DATABASE_PATH + 'logs' + separator


def local_data_saver(path: str = None, data = None, *, is_cache = False):
    from nef.utils import get_hash_of_timestamp
    if path is None:
        path = RESOURCE_PATH + get_hash_of_timestamp()

    if is_cache:
        path = CACHE_PATH + get_hash_of_timestamp()

    if data is None:
        return -1
    import numpy as np
    from scipy import sparse
    if isinstance(data, np.ndarray):
        if not path.endswith('npy'):
            path += '.npy'
        np.save(path, data)
    elif isinstance(data, sparse.coo_matrix):
        if not path.endswith('npz'):
            path += '.npz'
        sparse.save_npz(data, path)
    else:
        raise ValueError(f'Unsupported data tyoe {data.__class__.__name__} saving.')
    return path


def remote_data_saver(path: str = None, data = None, hostname = '127.0.0.1', port = 22,
                      pkey = None):
    from .sftp import sftp_upload
    if ':' not in path:
        return local_data_saver(path, data)
    local_path = local_data_saver(data = data, is_cache = False)
    sftp_upload(local_path, path, hostname, port, pkey)
    return path


def local_data_loader(path_: str):
    if not os.path.isfile(path_):
        path_ = RESOURCE_PATH + path_
    if path_.endswith('npy'):
        return np.load(path_)
    elif path_.endswith('npz'):
        return sparse.load_npz(path_)
    else:
        raise NotImplementedError(f'`data_loader` does not {path_} loading. ')
