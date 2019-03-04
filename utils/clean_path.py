#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : clean_path.py
# @Author: MoonKuma
# @Date  : 2019/3/4
# @Desc  : clean target path

import os
import os.path


def clean_target_path(file_path, file_type_exclude=('.py', '.gitignore'), recursive=True, report=True):
    files = os.listdir(file_path)
    for file_name in files:
        full_path = os.path.join(file_path, file_name)
        if os.path.isfile(full_path):
            f_name, ext = os.path.splitext(file_name)
            if ext not in file_type_exclude:
                if report:
                    print('[Removing]', os.path.abspath(full_path))
                os.remove(os.path.abspath(full_path))
        elif recursive and os.path.isdir(full_path):
            clean_target_path(full_path, file_type_exclude=file_type_exclude, recursive=recursive, report=report)

