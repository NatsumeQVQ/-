#coding:utf-8
import requests
import json
import time
from bs4 import BeautifulSoup
import csv
import random
from Tool import Tool

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#     'Cookie':'q_c1=c9c08ec2a3844479825b21c51c986c0f|1499177063000|1499177063000; _zap=b5a091bd-e67e-48fb-b8c2-09827f14c771; q_c1=c9c08ec2a3844479825b21c51c986c0f|1508039275000|1499177063000; d_c0="AJACGfmchwyPTtQDBM-W9MzV1A8ZUxWMbYo=|1508039276"; z_c0=Mi4xMS1rMUJnQUFBQUFBa0FJWi1aeUhEQmNBQUFCaEFsVk40WmNLV2dCVGJZdk5jMWJ5dkpqZDdiQXppQVYxVENVdnFn|1508051681|275f2b3651b89850a6d7c1856a827679c1a9a6eb; r_cap_id="NGE5ODM0YjU5M2JlNDZhZGIyYjc4YjlhMThmNmE3OTA=|1508051681|c352e352ef71c91fb914d983a4440c1585586a52"; cap_id="NmE3ZmExZDdmZmJlNDA5YzlhZWFjNzcxNDNhMmM3N2Q=|1508051681|126469ebe79fa389886ceb1a8ada59df63cf473a"; aliyungf_tc=AQAAAEtYPXzfzAQAnUqoe+EfTBupZhXI; s-q=%E4%B8%AD%E5%8D%B0%E5%AF%B9%E5%B3%99; s-i=2; sid=nrq5pong; __utma=51854390.1645812925.1508223374.1508240675.1508240675.3; __utmc=51854390; __utmz=51854390.1508223368.9.6.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20171015=1^3=entry_date=20170704=1; _xsrf=046fd901-0b26-4028-9614-4999a3a447d0'
# }
#base_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20&sort_by=default'

'''
#QuestionAnswers-answers > div:nth-child(1) > div > div.List-header > h4 > span
#QuestionAnswers-answers > div:nth-child(1) > div > div.List-header > h4 > span
'''
def get_contents(headers, number,fp):

    tool = Tool()

    writer = csv.writer(fp)

    url_web = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&limit=20&sort_by=default&offset='
    base_url = url_web.format(number)+'{}'
    url_number = 'https://www.zhihu.com/question/'+str(number)
    wb = requests.get(url_number, headers=headers)
    sp = BeautifulSoup(wb.text, 'lxml')
    num_sel = sp.select('#QuestionAnswers-answers > div > div > div.List-header > h4 > span')
    follower = sp.select('#root > div > main > div > div > div.QuestionHeader > div.QuestionHeader-content > div.QuestionHeader-side > div > div > div > button > div.NumberBoard-value')
    title = sp.select('#root > div > main > div > div > div.QuestionHeader > div.QuestionHeader-content > div.QuestionHeader-main > h1')
    browsed = sp.select('#root > div > main > div > div > div.QuestionHeader > div.QuestionHeader-content > div.QuestionHeader-side > div > div > div > div.NumberBoard-item > div.NumberBoard-value')
    if num_sel == []:
        return
    all_answer_num = int(num_sel[0].get_text().split()[0])
    if all_answer_num % 20 != 0:
        count = 1+all_answer_num//20
    else:
        count = all_answer_num//20
    for i in range(count):
        url_contents = base_url.format(i * 20)
        wb_data = requests.get(url_contents, headers=headers)
        js = json.loads(wb_data.content)
        for each in js['data']:
            con = tool.replace(each['content'])
            timestamp = each['created_time']  # 转换成localtime
            time_local = time.localtime(timestamp)  # 转换成新的时间格式
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            times = time_local.tm_mon + time_local.tm_mday/100
            if(times < 6.18 or times > 8.28):
                pass
            else:
                writer.writerow([title[0].get_text(), follower[0].get_text(), browsed[0].get_text(), dt,con])
                print(title[0].get_text(), follower[0].get_text(), browsed[0].get_text(), dt, con)
    time.sleep(random.uniform(2, 4))