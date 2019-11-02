#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : spidering_with_thread.py
# @Author: MoonKuma
# @Date  : 2019/2/28
# @Desc  :

"""
Used for downloading wikipedia like websites;
This script will start with one root, download its html content, and then adding it's internal links into searching list
We also use a multi-thread techniques to speed-up
"""


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
from utils.clean_path import clean_target_path


save_path = 'file_saved/zh.moegirl'

clean_target_path(file_path=save_path, report=False)  # delete old results

root = 'https://zh.moegirl.org/%E7%99%BD%E5%AD%A6'
# root = 'http://www.google.com'  # use google to test time out. Guess why? XD

test_num = 200000

SLEEP_TIME = 0.5  # sleep if no job available
MAX_WORKER = 50  # worker in threadpool executor
TIME_OUT_ACQUIRING = 5  # acquiring key time out
TIME_OUT_HTTP = (2.0, 10.0)  # http connect/read time out
PAGES_NUM = 10  # default pages num


internal_links_result = list()  # links that have been computed
waiting_list = WaitingList(root=root, timeout=TIME_OUT_ACQUIRING)  # links in waiting
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=urllib3.Timeout(connect=TIME_OUT_HTTP[0], read=TIME_OUT_HTTP[1]))

info_dict = {'ROOT': root,
             'SLEEP_TIME': SLEEP_TIME,
             'MAX_WORKER': MAX_WORKER,
             'TIME_OUT_ACQUIRING': TIME_OUT_ACQUIRING,
             'TIME_OUT_HTTP': TIME_OUT_HTTP}


def assign_work(report=False):
    # assign one unhandled work from the waiting list
    link = waiting_list.pop_link()
    msg = 'Link:' + link + ', assigned to worker'
    print(msg)
    if link != "":
        # compute here
        result = do_work(link)
        msg = 'Link:' + link
        if result == 1:
            msg += ', Finished!'
        if result == 0:
            msg += ', Time Out!'
        if result == -1:
            msg += ', Error!'
        if report:
            print(msg)
        return result
    else:
        msg = 'Waiting list is empty! Wait for another ' + str(SLEEP_TIME)
        print(msg)
        time.sleep(SLEEP_TIME)
        return -2


def do_work(link):
    internal_links = get_current_internal(link, save_path)
    if internal_links is not None:
        if len(internal_links)>0:
            if internal_links[0] not in [0, -1]:
                # standard
                waiting_list.add_links(internal_links)
                return 1
            else:
                # time out
                return internal_links[0]
        else:
            return 1
    else:
        return -1


# to compute
def get_current_internal(current_link, save_path, path_only=True):
    current_link = quote(current_link, safe=string.printable)
    # for pages like wikipedia, we only need to save those with same path and params and query could be omitted
    link_path = current_link
    if path_only:
        parsed = parse.urlparse(current_link)
        link_path = parsed.scheme + '://' + parsed.netloc + parsed.path
    internal_links_result.append(link_path)
    internal_links_tmp = list()
    try:
        response = http.request('get', link_path) # here may throw a time out exception
        if response.status == 200:  # succeed in connection
            bs_obj = BeautifulSoup(response.data, "html.parser")
            content = read_content(bs_obj=bs_obj)
            save_content(file_path=save_path, content=content, url=link_path)
            internal_links_tmp = get_links_inside(bs_obj=bs_obj, url=link_path, path_only=path_only) # here may return none if the pages is to large to read
            return internal_links_tmp
    except urllib3.exceptions.MaxRetryError:
        return [0, current_link]  # [0] stands for time out after max retry
    except:
        return [-1, current_link]  # [-1] stands for other type of error



# test
def test(test_times=PAGES_NUM):
    time_0 = time.time()
    for i in range(0, test_times):
        assign_work()
    info_dict['Marked'] = waiting_list.get_length_marking()
    info_dict['Waiting'] = waiting_list.get_length_waiting()
    info_dict['Time cost'] = time.time() - time_0


# test inside threadpool
def test_threadpool(test_times=PAGES_NUM):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKER)
    future_list = list()
    # point to start
    time_0 = time.time()
    assign_work()
    for i in range(0, test_times):
        future = executor.submit(fn=assign_work)
        future_list.append(future)
    futures.wait(future_list)
    info_dict['Test times'] = test_times
    info_dict['Marked'] = waiting_list.get_length_marking()
    info_dict['Waiting'] = waiting_list.get_length_waiting()
    info_dict['Result length'] = len(future_list)
    result_dict = {'Success': 0, 'TimeOut': 0, 'Error': 0, 'No Job':0}
    for future in future_list:
        if future.result() == 1:
            result_dict['Success'] = result_dict['Success'] + 1
        if future.result() == 0:
            result_dict['TimeOut'] = result_dict['TimeOut'] + 1
        if future.result() == -1:
            result_dict['Error'] = result_dict['Error'] + 1
        if future.result() == -2:
            result_dict['No Job'] = result_dict['No Job'] + 1
    info_dict['Result'] = result_dict
    info_dict['Time cost'] = time.time() - time_0
    save_info()


# save info
def save_info(report=True):
    if report:
        for item in info_dict.items():
            print(item)
    file_loc = os.path.join(save_path, 'info')
    if not os.path.exists(file_loc):
        os.mkdir(file_loc)
    file_name = os.path.join(file_loc, 'info.txt')
    with open(file_name, 'w') as file_w:
        file_w.write(str(info_dict))

# test()
test_threadpool(test_num)

