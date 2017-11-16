import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import re
import time
import random

class Tool:
    RemoveImg = re.compile('<img.*?>| {7}|')  #默认先删除左边img，如果左边没有，再匹配右边7个空格
    RemoveAddr = re.compile('<a.*?>|</a>')  #删除链接标签
    ReplaceLine = re.compile('<tr>|<div>|</div></p>')  #把换行的标签替换成\n
    ReplaceTD = re.compile('<td>')  # 把制表替换为\t
    ReplacePara = re.compile('<p.*?>')  # 把段落开头替换为\n并在开头加两个空格
    ReplaceBR = re.compile('<br><br>|<br>')  # 把换行和双换行替换为\n
    RemoveTag = re.compile('<.*?>')  #把其余标签去掉
    RemoveSpace = re.compile(' ')  #把空格去掉
    RemoveEnter = re.compile('\\n')
    RemoveLetter = re.compile('[a-z]')
    def replace(self,x):
        x = re.sub(self.RemoveImg,"",x)
        x = re.sub(self.RemoveAddr,"",x)
        x = re.sub(self.ReplaceLine,"",x)
        x = re.sub(self.ReplaceTD,"",x)
        x = re.sub(self.ReplacePara,"",x)
        x = re.sub(self.ReplaceBR,"",x)
        x = re.sub(self.RemoveTag,"",x)
        x = re.sub(self.RemoveSpace,"",x)
        x = re.sub(self.RemoveEnter,"",x)
        x = re.sub(self.RemoveLetter,'',x)
        return x

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Cookie':'_zap=b5a091bd-e67e-48fb-b8c2-09827f14c771; q_c1=c9c08ec2a3844479825b21c51c986c0f|1508039275000|1499177063000; d_c0="AJACGfmchwyPTtQDBM-W9MzV1A8ZUxWMbYo=|1508039276"; z_c0=Mi4xMS1rMUJnQUFBQUFBa0FJWi1aeUhEQmNBQUFCaEFsVk40WmNLV2dCVGJZdk5jMWJ5dkpqZDdiQXppQVYxVENVdnFn|1508051681|275f2b3651b89850a6d7c1856a827679c1a9a6eb; r_cap_id="NGE5ODM0YjU5M2JlNDZhZGIyYjc4YjlhMThmNmE3OTA=|1508051681|c352e352ef71c91fb914d983a4440c1585586a52"; cap_id="NmE3ZmExZDdmZmJlNDA5YzlhZWFjNzcxNDNhMmM3N2Q=|1508051681|126469ebe79fa389886ceb1a8ada59df63cf473a"; _xsrf=fa20d1a7-d237-4cb2-8ee8-ab3a43521f89; __utma=51854390.1799435999.1508380123.1508652360.1508921650.9; __utmb=51854390.0.10.1508921650; __utmc=51854390; __utmz=51854390.1508921650.9.12.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20171015=1^3=entry_date=20170704=1; aliyungf_tc=AQAAAHcP/zMl5AoAFvKfcwarM0xMVugi; XSRF-TOKEN=2|e7ffea7d|819ed84d83ce8b4aca9bd84ed0d2de1e85cdc745829ad250869dd91cd3ccdf4fd699d244|1508921661'
}

def get_zhuanlan_content(headers, number,fp = None):
    writer = csv.writer(fp)
    tool = Tool()

    # url_web = 'https://zhuanlan.zhihu.com/api/posts/{}/comments?limit=10&offset='
    # base_url = url_web.format(number)+'{}'
    url_number = 'https://zhuanlan.zhihu.com/p/'+number
    request = requests.get(url_number, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    title = soup.select('head > title')
    content = soup.select('#react-root > div > div > div.Layout-main.av-card.av-paddingBottom.av-bodyFont.Layout-titleImage--normal > div.RichText.PostIndex-content.av-paddingSide.av-card')
    content = content[0].get_text()
    t = soup.select('#react-root > div > div > div.Layout-main.av-card.av-paddingBottom.av-bodyFont.Layout-titleImage--normal > div.PostIndex-header.av-paddingTop.av-card > div.PostIndex-author > div > time')
    t = t[0].get('datetime')
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.strptime(t[0:24],"%a %b %d %Y %H:%M:%S"))))
    likeCount = soup.select('#react-root > div > div > div.Layout-main.av-card.av-paddingBottom.av-bodyFont.Layout-titleImage--normal > div.PostIndex-footer > div.PostIndex-vote > button')
    likeCount = likeCount[0].get_text()
    commentCount = soup.select('#react-root > div > div > div.Layout-main.av-card.av-paddingBottom.av-bodyFont.Layout-titleImage--normal > div.PostComment > div.BlockTitle.av-marginLeft.av-borderColor.PostComment-blockTitle > span.BlockTitle-title')
    commentCount = commentCount[0].get_text().split()[0]
    # js = json.loads(soup.find(id='preloadedState').get_text())
    # database = js['database']['Post'][number]
    # content = database['content']
    # likeCount = database['likeCount']
    # commentCount = database['commentCount']
    # publishedTime = database['publishedTime'][0:10]
    comtent = tool.replace(content)
    writer.writerow([title[0].get_text(), likeCount, dt, content])
    print(title[0].get_text(), likeCount, dt, content)
    time.sleep(random.uniform(2, 4))
    # if commentCount == '还没有评论':
    #     # writer.writerow([title[0].get_text(), likeCount, publishedTime, content])
    #     print(title[0].get_text(), likeCount, time, content)
    #     return
    # else:
    #     writer.writerow([title[0].get_text(), likeCount, time, content])
    # all_comment_num = int(commentCount)
    # if all_comment_num % 10 != 0:
    #     count = 1+all_comment_num//10
    # else:
    #     count = all_comment_num//10
    # for i in range(count):
    #     url_contents = base_url.format(i * 10)
    #     wb_data = requests.get(url_contents, headers=headers)
    #     js = json.loads(wb_data.content)
    #     for each in js:
    #         con = tool.replace(each['content'])
    #         times = int(publishedTime[5:7])+int(publishedTime[8:10])/100
    #         if(times < 6.18 or times > 8.28):
    #             pass
    #         else:
    #             # writer.writerow([title[0].get_text(), likeCount, publishedTime, content,con])
    #             print(title[0].get_text(), likeCount, publishedTime, content,con)
    #     time.sleep(3)

# get_zhuanlan_content(headers,'28370015')