#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File    : blhx_avatar.py
# @Author  : MoonKuma
# @Date    : 2019/11/2
# @Desc   : 抓取碧蓝航线游戏及其画师

from bs4 import BeautifulSoup
import urllib3
import certifi

# STEP1 找到抓取的位置
"""
碧蓝航线舰娘图鉴
http://wiki.joyme.com/blhx/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4
随便点开一个舰娘吧（是主角，确信！）
http://wiki.joyme.com/blhx/%E4%BC%81%E4%B8%9A
通过检查（Chrome浏览器，右键希望观察的目标-检查N），或访问源码（右键-访问网页源代码）的方法找到需要的信息
    首先是画师
    <td colspan="2" style="background:#f9f593"><b>画师</b>
    <td colspan="2">八才提督<span class="smwsearch"><a href="/blhx/%E7%89%B9%E6%AE%8A:%E6%8C%89%E5%B1%9E%E6%80%A7%E6%90%9C%E7%B4%A2/%E7%94%BB%E5%B8%88/%E5%85%AB%E6%89%8D%E6%8F%90%E7%9D%A3" title="特殊:按属性搜索/画师/八才提督">+</a></span>
    <td style="width:20%"><b>微博</b>
    <td style="width:80%"><a target="_blank" rel="noreferrer noopener" class="external text" href="http://weibo.com/vihao">八才提督</a>
    看起来连画师的微博/P站地址都提供了，这真是太棒了
    然后是立绘图片
    <div class="tab_con active" style="position:relative;overflow:hidden"><img alt="企业立绘.jpg" src="http://p0.qhimg.com/dr/350__/t01f19500372dbefe76.jpg" width="350" height="525" data-file-name="企业立绘.jpg" data-file-width="350" data-file-height="525" />
    <div class="tab_con" style="position:relative;overflow:hidden"><img alt="企业换装.jpg" src="http://p9.qhimg.com/dr/350__/t01375963a08ac925dd.jpg" width="350" height="525" data-file-name="企业换装.jpg" data-file-width="350" data-file-height="525" />
    <p><img alt="企业换装2.jpg" src="http://p1.qhimg.com/dr/350__/t016ac07383f22c5f6d.jpg" width="350" height="525" data-file-name="企业换装2.jpg" data-file-width="350" data-file-height="525" />
    这样图片名字和图片就都定位了
"""
# 全局变量
SAVE_PATH = 'result/blhx/'
SAVE_NAME_SHIPS = 'blhx_ships.txt'
SAVE_NAME = 'blhx_illu.txt'
PIC_TITLE = 'BLHX'
HOME_PAGE = 'http://wiki.joyme.com'
MEMO_LOC = 'http://wiki.joyme.com/blhx/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4'

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=urllib3.Timeout(connect=2.0, read=10.0))
result = dict()

# STEP2 建立一个链接
def request_link(link_path):
    try:
        response = http.request('get', link_path)
        if response.status == 200:  # 200表示链接成功
            return response.data
    except:
        return None


# STEP3 解析其中内容
"""
保存两份文件，一份文档里面记录了画师的微博等信息，另一份记录保存图片和画师名字
"""
def read_content(data):
    bs_obj = BeautifulSoup(data, "html.parser")
    # 先找到画师吧
    illustrator = ''
    weibo = ''
    weibo_name = ''
    pixiv = ''
    pixiv_name = ''
    all_a = bs_obj.findAll('a')
    for a in all_a:
        if a.get_attribute_list('title') and a.get_attribute_list('title')[0] != None and a.get_attribute_list('title')[0].startswith('特殊:按属性搜索/画师/'):
            illustrator = repr(a.get_attribute_list('title')[0]).replace('特殊:按属性搜索/画师/','').replace('\'','')
        if a.get_attribute_list('href') and a.get_attribute_list('href')[0] != None:
            if a.get_attribute_list('href')[0].startswith('http://weibo.com/'):
                weibo = repr(a.get_attribute_list('href')[0]).replace('\'','').replace('\\','')
                weibo_name = repr(a.text).replace('\'','').replace('\\','')
            if a.get_attribute_list('href')[0].startswith('https://www.pixiv.net/member'):
                pixiv = repr(a.get_attribute_list('href')[0]).replace('\'','').replace('\\','')
                pixiv_name = repr(a.text).replace('\'','').replace('\\','')
    if illustrator not in result.keys():
        result[illustrator] = [weibo_name,weibo,pixiv_name,pixiv]
    # 然后再找找图片名字和图片(这里利用只有立绘图片的标准宽度是350的特性)
    all_img = bs_obj.findAll('img',{'width':'350'})
    for img in all_img:
        name = img.get_attribute_list('alt')[0]
        pic = img.get_attribute_list('src')[0]
        if name!=None and pic!=None:
            picture = http.request('GET', pic)
            save_path = SAVE_PATH + illustrator + '_' + PIC_TITLE + '_' + name
            with open(save_path, 'wb') as f:
                f.write(picture.data)
                f.close()

# STEP4 对目标列表进行抓取
def get_target_list(url_list):
    for url in url_list:
        print('Now requesting:' + url )
        data = request_link(url)
        if data!=None:
            read_content(data)
    save_path = SAVE_PATH + SAVE_NAME
    with open(save_path, 'w') as f:
        for key in result.keys():
            item = key + ',' + ','.join(result[key]) + '\n'
            f.write(item)

"""
# 测试一下吧
test = ['http://wiki.joyme.com/blhx/%E4%BC%81%E4%B8%9A']
get_target_list(test)
# 成功了呢！
"""
# 接下里需要查询所有的舰娘了(这个时间很长的，可以选择先把需要的地址保存出来，然后慢慢让他下载)

def get_urls(momo):
    ship_dict = dict()
    data = request_link(momo)
    bs_obj = BeautifulSoup(data, "html.parser")
    all_a = bs_obj.findAll('a')
    for a in all_a:
        if  a.get_attribute_list('title') and a.get_attribute_list('title')[0] != None and a.get_attribute_list('href')[0].startswith('/blhx/') :
            if not a.get_attribute_list('title')[0].endswith('.改'):
                title = repr(a.get_attribute_list('title')[0].replace('\'','').replace('\\',''))
                herf = repr(a.get_attribute_list('href')[0]).replace('\'','').replace('\\','')
                if title not in ship_dict.keys():
                    ship_dict[title] = HOME_PAGE + herf
    save_path = SAVE_PATH + SAVE_NAME_SHIPS
    with open(save_path, 'w') as f:
        for key in ship_dict.keys():
            item = key + ',' + ship_dict[key] + '\n'
            f.write(item)
    return ship_dict


# 开始运行吧
url_dict = get_urls(MEMO_LOC)
visit_set = set()
for url_name in url_dict.keys():
    if url_dict[url_name] in visit_set:
        continue
    visit_set.add(url_dict[url_name])
get_target_list(visit_set)
# 剩下就是漫长的等待了

















