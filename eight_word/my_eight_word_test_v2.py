# coding: utf-8
import os
from datetime import datetime, timedelta
from multiprocessing import Pool
import multiprocessing
from nt import chdir
from io import open
from datetime import datetime

heaven = {1: '甲', 2: '乙', 3: '丙', 4: '丁', 5: '戊', 6: '己', 7: '庚', 8: '辛', 9: '壬', 10: '癸'}
earth = {1: '子', 2: '丑', 3: '寅', 4: '卯', 5: '辰', 6: '巳', 7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥'}


def calc_eight_word(dt):
    y = dt.year
    m = dt.month
    d = dt.day
    h = dt.hour
    mi = dt.minute
    hour_ts = int(dt.timestamp() / 60 / 60 + 8)
    datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S')

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

    eight_word = day_word + hour_word
    print datetime_str + ' -> ' + eight_word
    row = [datetime_str, str(dt.year), str(dt.month), str(dt.day), str(dt.hour), str(dt.minute),
           day_word, hour_word, eight_word]
    line = ','.join(row)
    return unicode(line + '\n')


def write_to_file(line):
    file = open(file_path, 'a', encoding='utf-8')
    file.write(line)
    file.close()


if __name__ == '__main__':
    start = datetime.now()
    print start
    print ''
    start_time = datetime(2023, 1, 1, 0, 30)
    end_time = datetime(2023, 1, 1, 23, 59)
    delta = timedelta(hours=1)
    time_list = []
    while start_time <= end_time:
        time_list.append(start_time)
        start_time += delta

    file_path = 'D:\\Projects\\python_projects\\DA_and_ML\\eight_word\\eight_word_26.txt'
    os.chdir(os.path.dirname(file_path))
    header = ['datetime', 'year', 'month', 'day', 'hour', 'minute',
              'day_word', 'hour_word', 'eight_word']
    f = open(file_path, 'w', encoding='utf-8')
    f.write(unicode(','.join(header) + '\n'))
    f.close()

    pool = Pool()
    for t in time_list:
        pool.apply_async(calc_eight_word, (t,), callback=write_to_file)
    pool.close()
    pool.join()

    end = datetime.now()
    print('')
    print(end)
    print('time cost:', (end - start))
