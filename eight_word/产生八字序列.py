# coding: utf-8
import datetime

heaven = {1: '甲', 2: '乙', 3: '丙', 4: '丁', 5: '戊', 6: '己', 7: '庚', 8: '辛', 9: '壬', 10: '癸'}
earth = {1: '子', 2: '丑', 3: '寅', 4: '卯', 5: '辰', 6: '巳', 7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥'}


def get_year_word(year: int):
    if year < 2000:
        print('年份错误，请计算2000年后的八字')
    else:
        yh = (year - 3) % 10 + 10
        if yh > 10:
            yh = yh % 10
        ye = (year - 3) % 12
        year_word = heaven[yh] + earth[ye]
        return year_word


def get_day_of_year(year: int, month: int, day: int):
    date = datetime.date(year, month, day)
    day_of_year = int(date.strftime('%j'))
    return day_of_year


def get_day_word(year: int, month: int, day: int):
    day_num = get_day_of_year(year, month, day)
    dh = (day_num - 5) % 10
    de = (day_num - 5) % 12 + 12
    if de > 12:
        de = de % 12
    day_word = heaven[dh] + earth[de]
    return day_word


def get_hour_word(year: int, month: int, day: int, hour: int, minute: int):
    day_num = get_day_of_year(year, month, day)
    dh = (day_num - 5) % 10
    he = (hour * 60 + minute) // 120 + 1
    hh = (dh * 2 + he - 2) % 10
    if hh > 10:
        hh = hh % 10
    hour_word = heaven[hh] + earth[he]
    return hour_word


if __name__ == '__main__':
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day
    h = datetime.datetime.now().hour
    mi = datetime.datetime.now().minute
    print(get_year_word(y))
    print(get_day_word(y, m, d))
    print(get_hour_word(y, m, d, h, mi))
