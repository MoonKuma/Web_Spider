#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : spidering_simple.py
# @Author: MoonKuma
# @Date  : 2019/2/25
# @Desc  : a simple version for crawling across website through a recursion
# This is suitable for simple cases. If the recursion caused a stack overflow when the website itself is too deep, or
# the procedure cost too much time, you may need a developed (sophisticate) way of doing this.
# See the list + threading method :

from search_across_website.web_crawler_methods import *
import urllib3
import certifi
from bs4 import BeautifulSoup
from urllib.parse import quote
import string
import sys
import gc
import time
import traceback

MAX_DEPTH = 2  # max depth, setting max depth= 10 will cost more than 1 hour of running
# MAX_DEPTH = sys.getrecursionlimit() - 10  # get max depth of current system

internal_links_result = []  # for those have been computed
untouched_links = []

root_website = 'https://zh.moegirl.org/%E7%99%BD%E5%AD%A6'
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
save_path = 'file_saved/zh.moegirl'


def get_current_internal(current_link, depth=0, path_only=True):
    current_link = quote(current_link, safe=string.printable)
    # for pages like wikipedia, we only need to save those with same path, and params and query could be omitted
    link_path = current_link
    if path_only:
        link_path = parse.urlparse(current_link).path
    if link_path in internal_links_result or depth >= MAX_DEPTH:
        if depth >= MAX_DEPTH:
            if link_path not in untouched_links:
                untouched_links.append(link_path)
        return 0
    internal_links_result.append(link_path)
    response = http.request('get', current_link)
    if response.status == 200:  # succeed in connection
        bs_obj = BeautifulSoup(response.data, "html.parser")
        content = read_content(bs_obj=bs_obj)
        save_content(file_path=save_path, content=content, url=current_link)
        internal_links_tmp = get_links_inside(bs_obj=bs_obj, url=current_link)
        # need to manually clear bs_obj and receive here to clean the ram
        del bs_obj
        del response
        # gc.collect()
        for links in internal_links_tmp:
            get_current_internal(links, depth=depth+1)
    return 0

start_time = time.time()
err_msg = ""
try:
    get_current_internal(current_link=root_website)
except:
    msg = 'Error after computing:' + str(len(internal_links_result))
    print(msg)
    err_msg = traceback.format_exc()
    print(err_msg)

end_time = time.time()
time_cost = end_time - start_time

# clean untouched url
for url in untouched_links:
    if url in internal_links_result:
        untouched_links.remove(url)

msg_finish = 'Finished! with time cost:' + str(time_cost) + ', read internal links :' + str(len(internal_links_result)) + ', untouched links:' + str(len(untouched_links))
print(msg_finish)
info = {'time_cost': time_cost,
        'len(internal_links_result)': len(internal_links_result),
        'len(untouched_links)': len(untouched_links),
        'root_website': root_website,
        'save_path': save_path,
        'MAX_DEPTH': MAX_DEPTH,
        'err_msg': err_msg}
# save other info
file_name = 'file_saved/zh.moegirl/info/info.txt'

with open(file_name, 'w') as file_w:
    file_w.write(str(info))
