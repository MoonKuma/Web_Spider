#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : methods.py
# @Author: MoonKuma
# @Date  : 2019/3/25
# @Desc  : some common methods in file io

import os


def get_file_name(file_name_full, fetch='file_head'):
    """
    split file and get certain parts
    :param file_name_full: file name
    :param fetch: type of fetch
    :return: file_path / file_name / file_head / file_ext
    """
    file_path, file_name = os.path.split(file_name_full)
    file_head, file_ext = os.path.splitext(file_name)
    if fetch == 'file_path':
        return file_path
    if fetch == 'file_name':
        return file_name
    if fetch == 'file_head':
        return file_head
    if fetch == 'file_ext':
        return file_ext
    if fetch == 'all':
        return [file_path, file_name,file_head, file_ext]


def save_iterable(file_path, iterable,  split=',', over_written=True):
    """
    save iterable object
    :param file_path: save path
    :param iterable: the object
    :param split: split by, like ',' or '\n'
    :param over_written: is overwrite
    :return: 0/1 as failed/succeed
    """
    msg = ''
    if os.path.exists(file_path):
        msg += '[WARNING] Saving File Exist,'
    if not over_written:
        msg += 'SKIPPED:' + file_path
        print(msg)
        return 0
    msg += 'WRITTEN:' + file_path
    print(msg)
    with open(file_path,'w',encoding='utf-8') as w_file:
        str2wri = split.join(iterable)
        w_file.write(str2wri)
    return 1


def save_info_dict(info_dict, file_path, over_written=True):
    """
    This is the version of saving dict info
    """
    return save_iterable(file_path=file_path,iterable=info_dict.items(),split='\n', over_written=over_written)


def count_lines(file_name):
    """
    Count line number of certain text file (\n as a line)
    :param file_name: file name
    :return: line count
    """
    count = 0
    with open(file_name, 'r', encoding='utf-8') as file_to_count:
        line = file_to_count.readline()  # iterable obj
        while line:
            count +=1
            line = file_to_count.readline()
    return count
