#coding:utf-8
from bs4 import BeautifulSoup
import requests
from contents import get_contents
import json
from zhuanlan import get_zhuanlan_comment
from me import get_zhuanlan_content
#模拟登陆
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Cookie':'q_c1=c9c08ec2a3844479825b21c51c986c0f|1499177063000|1499177063000; _zap=b5a091bd-e67e-48fb-b8c2-09827f14c771; q_c1=c9c08ec2a3844479825b21c51c986c0f|1508039275000|1499177063000; d_c0="AJACGfmchwyPTtQDBM-W9MzV1A8ZUxWMbYo=|1508039276"; z_c0=Mi4xMS1rMUJnQUFBQUFBa0FJWi1aeUhEQmNBQUFCaEFsVk40WmNLV2dCVGJZdk5jMWJ5dkpqZDdiQXppQVYxVENVdnFn|1508051681|275f2b3651b89850a6d7c1856a827679c1a9a6eb; r_cap_id="NGE5ODM0YjU5M2JlNDZhZGIyYjc4YjlhMThmNmE3OTA=|1508051681|c352e352ef71c91fb914d983a4440c1585586a52"; cap_id="NmE3ZmExZDdmZmJlNDA5YzlhZWFjNzcxNDNhMmM3N2Q=|1508051681|126469ebe79fa389886ceb1a8ada59df63cf473a"; aliyungf_tc=AQAAAIHC00Sj9QkA9Uqoe1Bac/ewSg0z; s-q=%E4%B8%AD%E5%8D%B0; s-i=1; sid=56hvaa88; __utma=51854390.1799435999.1508380123.1508938394.1509015374.12; __utmb=51854390.0.10.1509015374; __utmc=51854390; __utmz=51854390.1509015374.12.14.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20171015=1^3=entry_date=20170704=1; _xsrf=0cd10b7d-47f9-4d52-99cd-799b1f5da928'
}
base_url = "https://www.zhihu.com/r/search?q=%E4%B8%AD%E5%8D%B0&correction=1&type=content&offset={}"    #搜索页面动态加载url
def search_wb(base_url):
    links = []
    for i in range(1000):
        url = base_url.format(i * 10)
        wb = requests.get(url, headers=headers)
        js = json.loads(wb.content)
        if not js['htmls']:
            break
        for each in js['htmls']:
            soup = BeautifulSoup(each, 'lxml')
            links += soup.select('a.js-title-link')
    print('end')
    return links
links = search_wb(base_url)
zhuanlan = []

with open('问题.csv','w',encoding='utf_8_sig') as fp:
    for no in links:
        if 'zhuanlan' in no.get('href'):
            zhuanlan.append(no.get('href')[29:37])
        else:
            number = no.get('href')[10:18]
            get_contents(headers,number,fp)

with open('专栏文章.csv','w',encoding='utf_8_sig') as f:
    for num in zhuanlan:
        get_zhuanlan_content(headers,num,f)

with open('专栏评论.csv','w',encoding='utf_8_sig') as f:
    for num in zhuanlan:
        get_zhuanlan_comment(headers,num,f)