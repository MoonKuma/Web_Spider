#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : spidering_with_thread.py
# @Author: MoonKuma
# @Date  : 2019/2/28
# @Desc  : here we design another spidering structure


from search_across_website.web_crawler_methods import *
from search_across_website.WaitingList import WaitingList
from concurrent.futures import ThreadPoolExecutor
import urllib3
import certifi
from bs4 import BeautifulSoup
from urllib.parse import quote
import string
import sys
import gc
import time
import traceback
from concurrent import futures


save_path = 'file_saved/zh.moegirl'
root = 'https://zh.moegirl.org/%E7%99%BD%E5%AD%A6'

MAX_WEB_NUM = 1000  # the max num for computing
SLEEP_TIME = 0.1
MAX_WORKER = 10  # worker in threadpool executor
PAGES_NUM = 100 # how many target pages are needed

internal_links_result = list()  # links that have been computed
waiting_list = WaitingList(root=root)  # links in waiting
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def assign_work():
    # assign one unhandled work from the waiting list
    link = waiting_list.pop_link()
    msg = 'Link:' + link + ', assigned to worker'
    print(msg)
    if link != "":
        # compute here
        do_work(link)
        msg = 'Link:' + link + ', Finished!'
        print(msg)
        return 1
    else:
        time.sleep(SLEEP_TIME)
        return 0


def do_work(link):
    internal_links = get_current_internal(link, save_path)
    waiting_list.add_links(internal_links)


# to compute
def get_current_internal(current_link, save_path, path_only=True):
    current_link = quote(current_link, safe=string.printable)
    # for pages like wikipedia, we only need to save those with same path and params and query could be omitted
    link_path = current_link
    if path_only:
        parsed = parse.urlparse(current_link)
        link_path = parsed.scheme + '://' + parsed.netloc + parsed.path
    internal_links_result.append(link_path)
    response = http.request('get', link_path)
    internal_links_tmp = list()
    if response.status == 200:  # succeed in connection
        bs_obj = BeautifulSoup(response.data, "html.parser")
        content = read_content(bs_obj=bs_obj)
        save_content(file_path=save_path, content=content, url=link_path)
        internal_links_tmp = get_links_inside(bs_obj=bs_obj, url=link_path, path_only=path_only)
    return internal_links_tmp


# test
def test(test_times=PAGES_NUM):
    time_0 = time.time()
    for i in range(0, test_times):
        assign_work()
    print('Marked:', waiting_list.get_length_marking())
    print('Waiting:', waiting_list.get_length_waiting())
    print('Time cost: ', time.time()-time_0)


# test inside threadpool
def test_threadpool(test_times=PAGES_NUM):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKER)
    future_list = list()
    # point to start
    time_0 = time.time()
    assign_work()
    for i in range(0, test_times-1):
        future = executor.submit(fn=assign_work)
        future_list.append(future)
    futures.wait(future_list)
    print('Marked:', waiting_list.get_length_marking())
    print('Waiting:', waiting_list.get_length_waiting())
    print('Time cost: ', time.time() - time_0)

test()

