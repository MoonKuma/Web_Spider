#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : web_crawler_methods.py
# @Author: MoonKuma
# @Date  : 2019/2/26
# @Desc  : commonly used web crawling related methods inside this program

import re
import os
import copy
from urllib import parse
from utils.md5_transfer import md5_transfer
from urllib.parse import quote
import string

def get_url_root(url):
    """
    Get root for current url
    :param url: full url link, eg : https://123/456/789.php
    :return: url root link, eg https://123
    """
    parse_url = parse.urlparse(url)
    url_root = parse_url.scheme + '://' + parse_url.netloc
    return url_root


def get_links_inside(bs_obj, url, type_of_link='internal', path_only=True):
    """
    Usd for getting all internal/external/both links inside certain bs object
    Internal links
    Two types of links are regarded as internal links according to the HTTP.
    Those start with "/", which point to a direct page of the same location.
    Or those start with the currentURL, which point to some other path within the same website

    :param bs_obj: a beautiful soup object for compute
    :param url: the url to compute
    :param type_of_link: default is internal for internal links. other acceptable input include ['']
    :param path_only: if True, only save the path (no query or parameters) of those links inside
    :return: a list including all requested links inside the all_links object (this may be empty)
    """
    root_url = get_url_root(url)
    result_links = set()
    links = bs_obj.findAll("a")
    if type_of_link == 'internal':
        links = bs_obj.findAll("a", href=re.compile("^(/|.*" + root_url + ")"))
    elif type_of_link == 'external':
        links = bs_obj.findAll("a", href=re.compile("^(http|www)((?!"+root_url+").)*$"))
    for link in links:
        if link.attrs['href'] is not None and link.attrs['href'] :
            if link.attrs['href'].startswith("/"):
                link_add = root_url + link.attrs['href']
            else:
                link_add = link.attrs['href']
            link_add = quote(link_add, safe=string.printable)
            if path_only:
                parsed = parse.urlparse(link_add)
                link_add = parsed.scheme + '://' + parsed.netloc + parsed.path
            if link_add != "":
                result_links.add(link_add)
    return list(result_links)


def read_content(bs_obj, exclude_list = ('script', 'style'), target_list=(), remove_n = True, use_copy = False):
    """
    Used for reading all content information of certain beautiful soup object with excluding some special tags
    like 'script' and 'style' , or targeting certain special tags

    :param bs_obj: beautiful soup object of interesting
    :param exclude_list: tags to excludes, default is 'script' and 'style', you may adding new tags or remove them
    :param target_list: tags on target, if this is not empty, then the function will focus only on those targets
    :param remove_n: remove '\n' form content, default is True
    :param use_copy: whether use a copy of bs_obj, by default this is set as False, which means the procedure
                     of excluding certain tag is irreversible. Yet setting this as True will adding storing cost
    :return: content string

    """
    content = ""
    if len(target_list) != 0:
        for target in target_list:
            target_obj = bs_obj.find_all(target)
            content += target_obj.get_text()
    else:
        man_obj = bs_obj
        if use_copy:
            man_obj = copy.deepcopy(bs_obj)
        for exclude in exclude_list:
            for bs in man_obj.find_all(exclude):
                bs.extract()
        content = man_obj.get_text()
    if remove_n:
        content = content.replace('\n', '')
    return content


def save_content(file_path, url, content, over_write=True, report_progress=False):
    """
    Save content into files with md5(url) as path
    Using raw url as path will cause the following problems includes:
        * name is too long
        * name contain illegal characters, and its hard to replace them
    :param file_path: file save location
    :param url: full url
    :param content: content string
    :param over_write: overwrite file with same name
    :param report_progress: report saving progress
    :return: no return
    """
    url_path = md5_transfer(url) + '.txt'
    file = re.sub(r'[\/:*?"<>|]', ".", url_path)
    save_name = os.path.join(file_path, file)
    result_dict = dict()
    result_dict['url'] = url
    result_dict['content'] = content
    if os.path.exists(save_name):
        msg = '[WARNING] Find same md5 for url:' + str(url)
        if over_write:
            msg += ',execute overwriting'
            with open(save_name, 'w', encoding='utf-8') as file_w:
                file_w.write(str(result_dict))
        else:
            msg += ', file get omitted'
        print(msg)
    else:
        msg = 'Succeed in writing file for ' + str(url)
        with open(save_name, 'w', encoding='utf-8') as file_w:
            file_w.write(str(result_dict))
        if report_progress:
            print(msg)

