#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : testing_method.py
# @Author: MoonKuma
# @Date  : 2019/2/25
# @Desc  : testing modules used in the formal app

from urllib import parse
import urllib3
import certifi
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import string

url = 'https://zh.moegirl.org/%E7%99%BD%E5%AD%A6'
url = quote(url, safe=string.printable)  # this will helps solving the chinese url problem
# create a http reader
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
# request
response = http.request('get', url)  # this will cost some time for opening the pages (put this inside a thread worker)
if response.status == 200:  # succeed status:200
    print('Oh,yeah!')
    pass
# create a beautiful soup object
bsObj = BeautifulSoup(response.data, "html.parser")
d = bsObj.__copy__()
parseURL = parse.urlparse(url)
# get internal links (starts with / or contains the same net location)
currentURL = parseURL.scheme + '://' + parseURL.netloc
links = bsObj.findAll("a", href=re.compile("^(/|.*"+currentURL+")"))
# write them
internalLinks = []
for link in links:
    if link.attrs['href'] is not None and link.attrs['href'] not in internalLinks:
        if link.attrs['href'].startswith("/"):
            internalLinks.append(currentURL + link.attrs['href'])
        else:
            internalLinks.append(link.attrs['href'])
print('len(internalLinks):' + str(len(internalLinks)))
# save only the content
# yet we don't need content of style or script
print('How many script:', str(len(bsObj.find_all('script'))))
for bs in bsObj.find_all('script'):
    bs.extract()
print('How many script now:', str(len(bsObj.find_all('script'))))
print('How many style:', str(len(bsObj.find_all('style'))))
for bs in bsObj.find_all('style'):
    bs.extract()
print('How many style now:', str(len(bsObj.find_all('style'))))
print((bsObj.get_text()).strip()) # this should be pure content
# clean \n if necessary
content = (bsObj.get_text()).replace('\n','')
# save doc
save_file = 'file_saved/test_save/'
save_name = 'test.txt'
with open(save_file+save_name, 'w', encoding='utf-8') as w_file:
    for bs_x in bsObj:
        w_file.write(content)
