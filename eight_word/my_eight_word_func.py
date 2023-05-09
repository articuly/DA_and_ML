# coding: utf-8
import os
from datetime import datetime, timedelta
from multiprocessing import Pool
import multiprocessing
import csv
from datetime import datetime
from pytz import timezone as tz
from skyfield import almanac
from skyfield import almanac_east_asia
from skyfield import api

heaven = {1: '甲', 2: '乙', 3: '丙', 4: '丁', 5: '戊', 6: '己', 7: '庚', 8: '辛', 9: '壬', 10: '癸'}
earth = {1: '子', 2: '丑', 3: '寅', 4: '卯', 5: '辰', 6: '巳', 7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥'}


def calc_eight_word(dt: datetime):
    y = dt.year
    m = dt.month
    d = dt.day
    h = dt.hour
    mi = dt.minute
    hour_ts = int(dt.timestamp() / 60 / 60 + 8)
    datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S')

    # solar_terms_list
    utc_time = dt.astimezone(tz('Asia/Shanghai'))
    ts = api.load.timescale()
    sky_utc_time = ts.utc(utc_time)
    eph = api.load('de421.bsp')
    start_time = ts.utc(y, 1, 1)
    end_time = ts.utc(y, 12, 31)
    time, enum = almanac.find_discrete(start_time, end_time, almanac_east_asia.solar_terms(eph))
    terms_list = list(zip(enum, time))

    # compare_solar_terms
    list_len = len(terms_list)
    solar_term_index = -1
    for i in range(0, list_len - 1):
        if sky_utc_time - terms_list[0][1] < 0:
            solar_term_index = terms_list[0][0] - 1
        elif sky_utc_time - terms_list[list_len - 1][1] >= 0:
            solar_term_index = terms_list[list_len - 1][0]
        elif sky_utc_time - terms_list[i][1] >= 0 and sky_utc_time - terms_list[i + 1][1] < 0:
            solar_term_index = terms_list[i][0]

    # test_spring_begin
    if sky_utc_time - terms_list[2][1] >= 0:
        is_after_spring_begin = True
    else:
        is_after_spring_begin = False

    # get_year_word
    yh = (y - 3) % 10 or 10
    ye = (y - 3) % 12
    if (not is_after_spring_begin) or (m == 1 and d == 1):
        yh = yh - 1
        if yh < 1:
            yh = 10
        ye = ye - 1
        if ye < 1:
            ye = 12
    # print(yh, ye, end=' ')
    year_word = heaven[yh] + earth[ye]

    # get_month_word
    me = (solar_term_index + 1) // 2 + 4
    if me > 12:
        me = me - 12
    if solar_term_index == 18 and m == 1:
        local_year = y - 1
    else:
        local_year = y
    local_yh = (local_year - 3) % 10 or 10
    local_me = me
    if me == 1:
        local_me = 13
    mh = (local_yh * 2 + local_me - 2) % 10 or 10
    # print(mh, me, end=' ')
    month_word = heaven[mh] + earth[me]

    # get_day_word
    dh = (int(hour_ts / 24) - 2) % 10 or 10
    de = (int(hour_ts / 24) + 6) % 12 or 12
    # print(dh, de, end=' ')
    day_word = heaven[dh] + earth[de]

    # get_hour_word
    hh = int((hour_ts + 11) / 2) % 10 or 10
    he = round((h * 60 + mi) / 120) + 1
    if he > 12:
        he = he % 12
    # print(hh, he, end=' ')
    hour_word = heaven[hh] + earth[he]

    eight_word = year_word + month_word + day_word + hour_word
    print(datetime_str + ' -> ' + eight_word)
    row = [datetime_str, str(dt.year), str(dt.month), str(dt.day), str(dt.hour), str(dt.minute),
           year_word, month_word, day_word, hour_word, eight_word]
    # line = ','.join(row)
    return row


def listener(q):
    '''listens for messages on the q, writes to file. '''
    with open(file_name, 'a', encoding='utf-8') as f:
        while True:
            m = q.get()
            if m == 'kill':
                f.write('killed')
                break
            f.write(str(m) + '\n')
            f.flush()


def simple_main(dt):
    return dt.strftime('%Y%m%d')


if __name__ == '__main__':
    start = datetime.now()
    print(start)
    print('')
    # start_time = datetime(2023, 1, 1, 0, 30)
    # end_time = datetime(2023, 1, 1, 23, 59)
    # delta = timedelta(hours=1)
    # time_list = []
    # while start_time <= end_time:
    #     time_list.append(start_time)
    #     start_time += delta
    #
    # word_dir = os.fsencode('D:\\Projects\\python_projects\\DA_and_ML\\eight_word')
    # file_name = 'eight_word_26.txt'
    # os.chdir(word_dir)
    # header = ['datetime', 'year', 'month', 'day', 'hour', 'minute',
    #           'year_word', 'month_word', 'day_word', 'hour_word', 'eight_word']
    # f = open(file_name, 'w', encoding='utf-8')
    # f.write(','.join(header) + '\n')
    # f.close()
    #
    # # must use Manager queue here, or will not work
    # manager = multiprocessing.Manager()
    # q = manager.Queue()
    # pool = Pool(multiprocessing.cpu_count() - 2)
    #
    # # put listener to work first
    # watcher = pool.apply_async(listener, (q,))
    #
    # # fire off workers
    # jobs = []
    # for t in time_list:
    #     job = pool.apply_async(calc_eight_word, (t, q))
    #     jobs.append(job)
    #
    # # collect results from the workers through the pool result queue
    # for job in jobs:
    #     job.get()
    #
    # # now we are done, kill the listener
    # q.put('kill')
    # pool.close()
    # pool.join()

    start_time = datetime(2023, 1, 1, 0, 30)
    end_time = datetime(2025, 12, 31, 23, 59)
    delta = timedelta(hours=1)
    time_list = []
    while start_time <= end_time:
        time_list.append(start_time)
        start_time += delta

    header = ['datetime', 'year', 'month', 'day', 'hour', 'minute',
              'year_word', 'month_word', 'day_word', 'hour_word', 'eight_word']
    file_name = 'eight_word_23.csv'
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for t in time_list:
            r = calc_eight_word(t)
            writer.writerow(r)

    end = datetime.now()
    print('')
    print(end)
    print('time cost:', (end - start))
