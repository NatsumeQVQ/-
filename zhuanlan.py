import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
from Tool import Tool

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#     'Cookie':'_zap=b5a091bd-e67e-48fb-b8c2-09827f14c771; q_c1=c9c08ec2a3844479825b21c51c986c0f|1508039275000|1499177063000; d_c0="AJACGfmchwyPTtQDBM-W9MzV1A8ZUxWMbYo=|1508039276"; z_c0=Mi4xMS1rMUJnQUFBQUFBa0FJWi1aeUhEQmNBQUFCaEFsVk40WmNLV2dCVGJZdk5jMWJ5dkpqZDdiQXppQVYxVENVdnFn|1508051681|275f2b3651b89850a6d7c1856a827679c1a9a6eb; r_cap_id="NGE5ODM0YjU5M2JlNDZhZGIyYjc4YjlhMThmNmE3OTA=|1508051681|c352e352ef71c91fb914d983a4440c1585586a52"; cap_id="NmE3ZmExZDdmZmJlNDA5YzlhZWFjNzcxNDNhMmM3N2Q=|1508051681|126469ebe79fa389886ceb1a8ada59df63cf473a"; _xsrf=fa20d1a7-d237-4cb2-8ee8-ab3a43521f89; __utma=51854390.1799435999.1508380123.1508652360.1508921650.9; __utmb=51854390.0.10.1508921650; __utmc=51854390; __utmz=51854390.1508921650.9.12.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20171015=1^3=entry_date=20170704=1; aliyungf_tc=AQAAAHcP/zMl5AoAFvKfcwarM0xMVugi; XSRF-TOKEN=2|e7ffea7d|819ed84d83ce8b4aca9bd84ed0d2de1e85cdc745829ad250869dd91cd3ccdf4fd699d244|1508921661'
# }

def get_zhuanlan_comment(headers, number,fp = None):

    tool = Tool()
    writer = csv.writer(fp)

    url_web = 'https://zhuanlan.zhihu.com/api/posts/{}/comments?limit=10&offset='   #专栏评论
    base_url = url_web.format(number)+'{}'
    url_number = 'https://zhuanlan.zhihu.com/p/'+number #专栏文章url
    request = requests.get(url_number, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    title = soup.select('head > title')
    commentCount = soup.select('#react-root > div > div > div.Layout-main.av-card.av-paddingBottom.av-bodyFont.Layout-titleImage--normal > div.PostComment > div.BlockTitle.av-marginLeft.av-borderColor.PostComment-blockTitle > span.BlockTitle-title')
    commentCount = commentCount[0].get_text().split()[0]
    if commentCount == '还没有评论':
        return
    all_comment_num = int(commentCount)
    if all_comment_num % 10 != 0:
        count = 1+all_comment_num//10
    else:
        count = all_comment_num//10
    for i in range(count):
        url_contents = base_url.format(i * 10)
        wb_data = requests.get(url_contents, headers=headers)
        js = json.loads(wb_data.content)
        for each in js:
            con = tool.replace(each['content'])
            writer.writerow([title[0].get_text(),con])
            print(title[0].get_text(),con)
    time.sleep(random.uniform(2,4))

# get_zhuanlan_comment(headers,'28047189')