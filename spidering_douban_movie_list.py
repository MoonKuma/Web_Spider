#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : spidering_douban.py
# @Author: MoonKuma
# @Date  : 2019/4/4
# @Desc  :

"""
Used for searching and downloading web page data from douban like (database based) website
This script is for downloading movie list
"""

# a simple version

from search_across_website.web_crawler_methods import *
import urllib3
import certifi
from urllib.parse import quote
import string
import traceback
import json
from utils.file_io import save_iterable





save_path = 'file_saved/douban/'

TIME_OUT_HTTP = (2.0, 10.0)  # http connect/read time out
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=urllib3.Timeout(connect=TIME_OUT_HTTP[0], read=TIME_OUT_HTTP[1]))


def request_recommended():
    """
    Request douban recommended movie list
    This will offer the movie id inside douban system like : https://movie.douban.com/subject/26924141/
    We then use such ID 26924141 to locate its comments
    :return: No return, but this will save out a result file
    """
    save_file = os.path.join(save_path, 'douban_movie_id')
    url_root = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=%{start_page}%'
    comment_start_page = get_next(start=0, step=20, max=2000)
    url_list = list()
    for current_page in comment_start_page:
        current_page = str(current_page)
        url_now = url_root.replace('%{start_page}%', current_page)
        current_link = quote(url_now, safe=string.printable)
        try:
            print('Requesting: ', current_link)
            response = http.request('get', current_link) # here may throw a time out exception
            if response.status == 200:  # succeed in connection
                data = response.data.decode(encoding='utf-8')
                json_data = json.loads(data)
                subjects = json_data['subjects']
                if isinstance(subjects,list) and len(subjects)>0:
                    for movie in subjects:
                        if isinstance(movie, dict) and 'url' in movie.keys():
                            url = movie['url']
                            if url not in url_list:
                                url_list.append(url)
                else:
                    break
        except urllib3.exceptions.MaxRetryError:
            print('urllib3.exceptions.MaxRetryError at ', current_link)  # [0] stands for time out after max retry
        except:
            traceback.format_exc()
            break
    if len(url_list)>0:
        save_iterable(file_path=save_file, iterable=url_list,  split='\n', over_written=True)


request_recommended()

