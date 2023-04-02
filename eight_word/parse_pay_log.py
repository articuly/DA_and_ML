# coding:utf-8
import csv
import re

from MyEightWord import EightWord
from skyfield_datetime_util import datetime_returns

# 读取祈愿记录文件
f = open('pay_log.txt', 'r', encoding='utf-8')
pay_log = f.readlines()
f.close()

# 打开CSV文件，写入表头
t = open('pay_log.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(t)
csv_writer.writerow(['name', 'times', 'year_to_day', 'hour_to_second', 'is_guarantee', 'eight_word'])

for i in pay_log:
    # 处理祈愿记录
    pre = i.split(' ')[0]
    hs = i.split(' ')[1]
    hs = re.search(r'\d+', hs).group()
    name_times = pre.split('：')[0]
    yd = pre.split('：')[1]
    name = re.search(r'[\u4e00-\u9fa5]+', name_times).group()
    times = re.search(r'\d+', name_times).group()
    if '大' in i:
        guarantee = 1
    else:
        guarantee = 0

    # 计算八字
    e = EightWord(*datetime_returns(yd, hs))
    eight_word = e.get_year_word() + e.get_month_word() + e.get_day_word() + e.get_hour_word()

    # 写入csv文件
    csv_writer.writerow([name, times, yd, hs, guarantee, eight_word])

t.close()
