#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : spidering_douban_comments.py
# @Author: MoonKuma
# @Date  : 2019/4/8
# @Desc  :

"""
Used for requesting douban comments of certain movie
url : https://movie.douban.com/subject/30163509/comments?start=0&limit=20&sort=new_score&status=P&percent_type=m
It looks like douban allow showing first 200 comments of each kind
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


percent_type_list = ['h', 'm', 'l']

target_url = 'https://movie.douban.com/subject/30163509/comments?start=%{start_page}%&limit=20&sort=new_score&status=P&percent_type=%{percent_type}%'

start_page = '0'
percent_type = 'h'

TIME_OUT_HTTP = (2.0, 10.0)  # http connect/read time out
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=urllib3.Timeout(connect=TIME_OUT_HTTP[0], read=TIME_OUT_HTTP[1]))

test_url = target_url.replace('%{start_page}%', start_page).replace('%{percent_type}%', percent_type)

response = http.request('get', test_url)
bs_obj = BeautifulSoup(response.data, "html.parser")
# get comments
comments = bs_obj.find_all("div", class_="comment")

com0 = comments[0]

# rank
com0.find_all("span",title="力荐")
# content
obj = com0.find_all("p", _class="")
content = obj[0].get_text()


