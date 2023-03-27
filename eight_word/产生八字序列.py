# coding: utf-8
from datetime import datetime, timedelta, date
from skyfield_get_solar_terms import get_solar_terms


class EightWord:
    heaven = {1: '甲', 2: '乙', 3: '丙', 4: '丁', 5: '戊', 6: '己', 7: '庚', 8: '辛', 9: '壬', 10: '癸'}
    earth = {1: '子', 2: '丑', 3: '寅', 4: '卯', 5: '辰', 6: '巳', 7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥'}

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int = 0):
        self.de = None
        self.day_word = None
        self.dh = None
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.day_of_year = 0
        self.yh = -1
        self.ye = -1
        self.mh = -1
        self.me = -1
        self.year_word = ''
        self.month_word = ''

    def get_day_of_year(self):
        the_date = date(self.year, self.month, self.day)
        self.day_of_year = int(the_date.strftime('%j'))

    def get_year_word(self):
        if self.year < 2000:
            print('年份错误，请输入2000年后的八字')
        else:
            self.yh = (self.year - 3) % 10 + 10
            if self.yh > 10:
                self.yh = self.yh % 10
            self.ye = (self.year - 3) % 12
            print(self.yh, self.ye, end=' ')
            self.year_word = EightWord.heaven[self.yh] + EightWord.earth[self.ye]

    def get_month_word(self):
        datetime_str = str(self.year) + str(self.month) + str(self.day) + ' ' + str(self.hour) + str(self.minute) + str(
            self.second)
        solar_term_index = get_solar_terms(datetime_str)
        self.me = (solar_term_index + 1) // 2 + 4
        if self.me >= 12:
            self.me = self.me - 12
        self.mh = (self.yh * 2 % 10 + self.month - 1) % 10
        if self.mh == 0:
            self.mh = 10
        print(self.mh, self.me, end=' ')
        self.month_word = EightWord.heaven[self.mh] + EightWord.earth[self.me]

    def get_day_word(self):
        self.get_day_of_year()
        self.dh = (self.day_of_year - 5) % 10
        if self.dh == 0:
            self.dh = 10
        de = (self.day_of_year - 5) % 12 + 12
        if self.de > 12:
            de = de % 12
        print(self.dh, self.de, end=' ')
        self.day_word = EightWord.heaven[self.dh] + EightWord.earth[self.de]


def get_hour_word(year: int, month: int, day: int, hour: int, minute: int):
    if hour >= 23:
        new_date = date(year, month, day) + timedelta(days=1)
        return get_hour_word(year, month, new_date.day, 0, minute)
    day_num = get_day_of_year(year, month, day)
    dh = (day_num - 5) % 10
    he = round((hour * 60 + minute) / 120) + 1
    if he > 12:
        he = he % 12
    hh = (dh * 2 + he - 2) % 10
    if hh == 0:
        hh = 10
    # print(hh, he, end=' ')
    hour_word = heaven[hh] + earth[he]
    return hour_word


if __name__ == '__main__':
    # y = datetime.now().year
    # m = datetime.now().month
    # d = datetime.now().day
    # h = datetime.now().hour
    # mi = datetime.now().minute
    # s = datetime.now().second
    # y = 2023
    # m = 3
    # d = 25
    h = 12
    mi = 30
    # print(f'{y} {m} {d} {h} {mi}:', end=' ', )
    # print(get_year_word(y), end=' ')
    # print(get_month_word(y, m, d, h, mi), end=' ')
    # print(get_day_word(y, m, d), end=' ')
    # print(get_hour_word(y, m, d, h, mi))

    for y in range(2020, 2024):
        for m in range(1, 13):
            for d in [8, 28]:
                print(f'{y} {m} {d} {h} {mi}:', end=' ', )
                print(get_year_word(y), end=' ')
                print(get_month_word(y, m, d, h, mi), end=' ')
                print(get_day_word(y, m, d), end=' ')
                print(get_hour_word(y, m, d, h, mi))
