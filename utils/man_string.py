#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : man_string.py
# @Author: MoonKuma
# @Date  : 2019/3/26
# @Desc  : string related methods


import re
import string


def filter_string(string_line, ban_list=list(string.printable)):
    """
    :param string_line: string to filter
    :param ban_list: characters need to be removed
    :return: filtered string
    """
    filter_line = filter(lambda x: x not in ban_list, string_line)
    return ''.join(filter_line)


def select_reg(text, regex=u"[\u4E00-\u9FA5]+", splitter=' '):
    """
    using regulation expression to select certain characters
    :param text: text to sift
    :param regex: re regex patten, the default one regex=u"[\u4E00-\u9FA5]+" is for sifting chinese
    :return: string after sifting
    """
    result = ''
    res = re.findall(regex, text)
    if len(res)>0:
        result = splitter.join(res)
    return result
