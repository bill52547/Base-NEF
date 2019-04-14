# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: nef
@file: doc_generator.py
@date: 4/13/2019
@desc:
'''
from getpass import getuser
import os
import sys
import time
from nef.utils import tqdm, any_type_loader
import matplotlib

matplotlib.use('Agg')
timestamp = time.time()
datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
datetime_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(int(timestamp)))

author = getuser()


def title_block_gen():
    title_block = f"""
# NEF AutoDoc {datetime}
- Author: {author} 
- Generation time: {datetime}
- Operation system: {sys.platform}
- OS language: {os.environ['LANG']}
- Duration: 0.0 sec
- Total errors: 0
- Total warning: 0
- Description: 




\pagebreak


"""
    return [title_block]


def _text_gen_as_table(dct: dict = {}):
    out_text = ['|key|values|\n|:---|:---|\n']
    for key, val in dct.items():
        if not isinstance(val, dict):
            if isinstance(val, str) and len(val) > 30:
                out_text.append(f"| {key} | Ignored |\n")
            else:
                out_text.append(f"| {key} | {val} |\n")
        else:
            out_text.append(f"| {key} | {'Ignored'} |\n")

    return out_text


def block_gen(dct: dict = {}, *, foldername = './'):
    out_text = []

    print('Generating text blocks...')
    for key, val in tqdm(dct.items()):
        out_text.append(f'### Name: {key}\n')
        out_text += _text_gen_as_table(val)
        if 'data' in val:
            if not os.path.isdir(foldername + 'figures'):
                os.mkdir(foldername + 'figures')

            url = val['data']
            if url.endswith('npy'):
                from matplotlib import pyplot as plt
                data = any_type_loader(url.split(':')[-1])
                shape = data.shape
                plt.figure(figsize = (30, 10))
                plt.subplot(131)
                plt.imshow(data[:, :, int(shape[2] / 2)])
                plt.subplot(132)
                plt.imshow(data[:, int(shape[1] / 2), :].transpose())
                plt.subplot(133)
                plt.imshow(data[int(shape[0] / 2), :, :].transpose())
                img_path = foldername + 'figures/' + key + 'data.png'
                plt.savefig(img_path)
                # out_text.append(f'![]({key}data.png)\n')
                out_text.append(f"![This is the caption]({img_path})\n")
                out_text.append(f"\\pagebreak\n\n")

    return out_text


def statistic_block_gen(dct: dict = {}):
    out_text = []

    key_set = set()
    for name, sub_dct in dct.items():
        for key, val in sub_dct.items():
            if len(val) < 30:
                key_set.add(key)
            #
            # try:
            #     float(val)
            #     key_set.add(key)
            # except:
            #     pass
    col_names = ['|name ', '|:---']
    for key in key_set:
        col_names[0] += '|' + key + ''
    else:
        col_names[0] += '|\n'
    for _ in key_set:
        col_names[1] += '|:---'
    else:
        col_names[1] += '|\n'
    out_text += col_names

    for name, sub_dct in dct.items():
        row = '| ' + name + ' '
        for key in key_set:
            if key in sub_dct:
                row += '|' + str(sub_dct[key]) + ''
            else:
                row += '|-'
        else:
            row += '|\n'

        out_text += [row]

    return out_text


def doc_gen(dct: dict = {}, path: str = None):
    import pypandoc
    if path is None:
        path = './doc_gen-' + datetime_str + '.md'
    if path.endswith('/'):
        path += './doc_gen-' + datetime_str + '.md'
    foldername = os.path.dirname(os.path.abspath(path)) + '/'
    out_text = title_block_gen()
    out_text += block_gen(dct, foldername = foldername)
    out_text += statistic_block_gen(dct)
    with open(path, 'w') as fout:
        fout.writelines(out_text)
    print('Converting MD to PDF...')
    pypandoc.convert_file(path, 'pdf', outputfile = path + '.pdf')
    return path
