# coding:utf-8
import time
import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests
from lxml import html
from urllib import parse
import csv
from redis import StrictRedis
import json

# 连接缓存数据库
redis = StrictRedis(host='127.0.0.1', port=6379)
# 1岗位搜索列表页面链接列表
links_list = list()
# 2岗位详情列表页面链接队列
job_links_queue = Queue()
# 3待保存数据队列
job_info_queue = Queue()
# 每次开始抓取清空缓存
redis.delete('crawled_links')

# 浏览器参数
cookie = 'guid=30031bf4916e0d8a62fa75ac4190404d; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60040000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60020000%2C030200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60020000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60030200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21'
headers = {'Host': 'search.51job.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Referer': 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
           'Cookie': cookie,
           'X-Requested-With': 'XMLHttpRequest'}
start_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
# 全局变量
keyword = 'python'
keyword = parse.quote(parse.quote(keyword))
pages = 100
# csv实例
csv_writer = csv.writer(open(f'{keyword}_jobs_all.csv', 'a', encoding='utf-8'))
# 将N页职位搜索页加入到列表中
for i in range(1, pages + 1):
    url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{i}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    links_list.append(url)


# 抓取列表提取链接，添加到队列，并过滤重复的链接
def extract_list_links():
    global headers
    for url in links_list:
        # 请求链接
        req = requests.get(url, timeout=5, headers=headers)
        # 获取内容，gbk解码
        data = req.content.decode('gbk')
        print('success loading', url)
        # 将json内容数据解析
        try:
            jobs = json.loads(data)
        except Exception as e:
            print(e)
        else:
            # 找到每一页的链接
            for i in range(len(jobs['engine_search_result'])):
                job_link = jobs['engine_search_result'][i]['job_href']
                job_links_queue.put(job_link)
            print('job_links_len:', job_links_queue.qsize())


# 获取所有页面dom对象
def get_page(url, headers):
    time.sleep(random.randint(1, 5))  # 防止过量访问
    try:
        res = requests.get(url=url, headers=headers)
        page = res.content.decode('gbk')
    except Exception as e:
        print(e)
        return None
    else:
        # 已经爬取的链接加入到redis记录
        redis.sadd('crawed_links', url)
    try:
        dom = html.document_fromstring(page)
    except Exception as e:
        print(e)
        return None
    return dom


# # 从页面提取有用信息
def extract_info():
    while True:
        try:
            refer = redis.srandmember('crawed_links', 1)[0].decode()
            # redis.srem('crawed_links', refer)
        except Exception as e:
            print(e)
            refer = start_url
        # 增加headers反爬
        global headers
        headers['Referer'] = refer
        # 各种信息的XPATH语法
        job_name_xpath = "//h1/@title"
        job_salary_xpath = "//div[@class='cn']/strong/text()"
        job_info_xpath = "//p[@class='msg ltype']"
        job_stars_xpath = "//div[@class='t1']/span[@class='sp4']/text()"  # list
        job_description_xpath = "//div[@class='bmsg job_msg inbox']/p/text()"  # list
        job_category_xpath = "//div[@class='bmsg job_msg inbox']/div/p[1]/a/text()"  # list
        job_contact_xpath = "//div[@class='bmsg inbox']/p/text()"
        company_introduction_xpath = "//div[@class='tmsg inbox']"
        company_name_xpath = "//div[@class='com_msg']"
        company_type_xpath = "//div[@class='com_tag']/p[1]"
        company_size_xpath = "//div[@class='com_tag']/p[2]"
        company_industry_xpath = "//div[@class='com_tag']/p[3]"
        company_url_xpath = "//p[@class='cname']/a[@class='catn']/@href"
        # 将网页变成dom对象
        try:
            job_link = job_links_queue.get()
            print('extracting_job_link:', job_link)
        except Exception as e:
            print(e)
        else:
            dom = get_page(job_link, headers=headers)
            if dom is None:
                return False
        # 用lxml解析dom对象
        try:
            job_name = dom.xpath(job_name_xpath)[0]
            job_salary = dom.xpath(job_salary_xpath)[0]
            job_info = dom.xpath(job_info_xpath)[0].text_content()
            job_stars = dom.xpath(job_stars_xpath)
            job_description = dom.xpath(job_description_xpath)
            job_category = dom.xpath(job_category_xpath)
            job_contact = dom.xpath(job_contact_xpath)[0]
            company_introduction = dom.xpath(company_introduction_xpath)[0].text_content().strip()
            company_name = dom.xpath(company_name_xpath)[0].text_content().strip()
            company_type = dom.xpath(company_type_xpath)[0].text_content()
            company_size = dom.xpath(company_size_xpath)[0].text_content()
            company_industry = dom.xpath(company_industry_xpath)[0].text_content().strip()
            company_url = dom.xpath(company_url_xpath)[0]
        except Exception as e:
            print(e, 'missing some values')
        else:
            print([job_name, job_salary, company_name])
            job_stars = ','.join(job_stars)
            job_description = ','.join(job_description)
            job_category = ','.join(job_category)
            job_info_queue.put([job_name, job_salary, job_info, job_stars, job_category, job_description, job_contact,
                                company_name, company_type, company_size, company_industry, company_introduction,
                                job_link, company_url])
            # print('job_info_queue_size', job_info_queue.qsize())


# 保存职位信息
def save_info():
    while True:
        try:
            job_info = job_info_queue.get()
        except Exception as e:
            print(e)
        else:
            csv_writer.writerow(job_info)


# 最多20个线程，根据任务不同，分配不同的数量
extract_list_links()
pool = ThreadPoolExecutor(max_workers=8)
for i in range(4):
    pool.submit(extract_info)
for i in range(4):
    pool.submit(save_info)

# extract_list_links()
# extract_info()
# save_info()
