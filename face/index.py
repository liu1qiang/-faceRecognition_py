#encoding=utf8
import requests
from bs4 import BeautifulSoup
import time
import redis
import json
pool = redis.ConnectionPool(host="127.0.0.1", port=6379,max_connections=1024,decode_responses=True)
conn = redis.Redis(connection_pool=pool)
# comments = []
# url = "http://tieba.baidu.com/f?kw=%E5%8D%8E%E5%8D%97%E5%86%9C%E4%B8%9A%E5%A4%A7%E5%AD%A6&fr=index&red_tag=y3160164477"
# wb_data = requests.get(url)
# soup = BeautifulSoup(wb_data.content,"lxml")
# Tags = soup.find_all('li', attrs={"class": 'j_thread_list clearfix'})
# for li in Tags:
#     comment = {}
#     b = li.find('span', attrs={"class": "frs-author-name-wrap"})
#     comment["author"] = b.text
#     a = li.find('a', attrs={"class": "j_th_tit"})
#     comment["title"] = a.text
#     # c = li.find('div', attrs={"class": "threadlist_abs threadlist_abs_onlyline "})
#     # comment["read"] = c.text.strip()
#     # d = li.find('span', attrs={"class": "threadlist_rep_num center_text"})
#     # comment["reply"] = d.text.strip()
#     print (comment)
#     comments.append(comment)
# with open(r'E:\6.txt', 'a+', encoding='utf-8') as f:
#     for word in comments:
#         f.write('标题：{} \t发帖人：{} \t\n'.format(word["title"],word['author']))
# 首页景点
# def create_city(url,filename):
#     # url= "https://www.tripadvisor.cn/Attractions-g60763-Activities-New_York_City_New_York.html"
#     url = url
#     wb_data = requests.get(url)
#     soup = BeautifulSoup(wb_data.content,"lxml")
#     Tags = soup.find_all('div',attrs={"class":"detail"})
#     comments = []
#     for details in Tags:
#         comment = {}
#         title = details.find("a",attrs={"class":"poiTitle"})
#         HP = details.find("a",attrs = {"class":"review_count"})
#         if HP != None:
#             print ("好评开始赋值")
#             comment['HP'] = HP.text 
#         if title != None:
#             print ("title开始赋值")
#             comment['title'] = title.text
#         comments.append(comment)
#         print (comment)
#     with open(r'E:\{}.txt'.format(filename), 'a+', encoding='utf-8') as f:
#         for content in comments:
#             f.write('景点：{} \t好评:{} \t\n'.format(content["title"],content['HP']))
# create_city("https://www.tripadvisor.cn/Attractions-g60763-Activities-New_York_City_New_York.html","纽约")

# 带有翻页的爬虫
def create_city_page(url,filename,HSKEY):
    print ("开始爬去:"+url+"网页内容")
    comments = []
    url = url
    con = 0
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.content,"lxml")
    Tags = soup.find_all("div",attrs={"class":"attraction_element"})
    for details in Tags:
        conment = {}
        name = details.find("div",attrs={"class":"listing_title"})
        HP = details.find("div",attrs={"class":"rs rating"})
        if name != None:
            strName = name.text.replace("\n","")
            strName2 =strName.replace("#taplc_dmo_attribute_to_collection_clarity_"+str(con)+" { display:none;}","")
            print (strName2)
            conment['name'] =strName2
            con +=1
        if HP != None:
            strHP =  HP.text.replace('\n',"")
            conment['HP'] = strHP
        comments.append(conment)
    print (comments)
    for content in comments:
        print ({'name:{},HP:{}'.format(content['name'],content["HP"])})
        conn.hset(HSKEY,content["name"],json.dumps({'name:{},HP:{}'.format(content['name'],content["HP"])}))
    redisObj = conn.hgetall(HSKEY)
    print (redisObj)
    # with open(r'E:\{}.txt'.format(filename), 'a+', encoding='utf-8') as f:
    #     for content in comments:
    #         f.write('景点：{} \t好评:{} \t\n'.format(content["name"],content['HP']))

def start(filename,start,end,HSKEY):
    startNum = 30
    for num in range (start,end):
        strURL = ""
        time.sleep(5)
        if num == 0:
            strURL = "https://www.tripadvisor.cn/Attractions-g60763-Activities-New_York_City_New_York.html#FILTERED_LIST"
            create_city_page(strURL,filename,HSKEY)
        else:
            strURL = 'https://www.tripadvisor.cn/Attractions-g60763-Activities-oa'+str(num * startNum)+'-New_York_City_New_York.html#FILTERED_LIST'
            create_city_page(strURL,filename,HSKEY)
start("纽约",0,1,"NEW_YORK")