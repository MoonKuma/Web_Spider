#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : md5_transfer.py
# @Author: MoonKuma
# @Date  : 2019/2/12
# @Desc  : use md5 to irreversibly cipher the name of participants

import hashlib
m2 = hashlib.md5()


def md5_transfer(input_str):
    m2.update(str(input_str).encode('utf-8'))
    return m2.hexdigest()
