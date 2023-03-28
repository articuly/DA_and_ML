# coding: utf-8
from datetime import datetime, timedelta, date
from skyfield_get_solar_terms import get_solar_terms


class EightWord:
    heaven = {1: '甲', 2: '乙', 3: '丙', 4: '丁', 5: '戊', 6: '己', 7: '庚', 8: '辛', 9: '壬', 10: '癸'}
    earth = {1: '子', 2: '丑', 3: '寅', 4: '卯', 5: '辰', 6: '巳', 7: '午', 8: '未', 9: '申', 10: '酉', 11: '戌', 12: '亥'}

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int = 0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.day_of_year = -1
        self.yh = -1
        self.ye = -1
        self.mh = -1
        self.me = -1
        self.dh = -1
        self.de = -1
        self.hh = -1
        self.he = -1
        self.year_word = ''
        self.month_word = ''
        self.day_word = ''
        self.hour_word = ''

    @staticmethod
    def get_day_of_year(year, month, day):
        the_date = date(year, month, day)
        day_of_year = int(the_date.strftime('%j'))
        return day_of_year

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
            return self.year_word

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
        return self.month_word

    def get_day_word(self):
        day_of_year = self.get_day_of_year(self.year, self.month, self.day)
        self.dh = (day_of_year - 5) % 10
        if self.dh == 0:
            self.dh = 10
        de = (self.day_of_year - 5) % 12 + 12
        if self.de > 12:
            de = de % 12
        print(self.dh, self.de, end=' ')
        self.day_word = EightWord.heaven[self.dh] + EightWord.earth[self.de]
        return self.day_word

    def get_hour_word(self):
        if self.hour >= 23:
            new_date = date(self.year, self.month, self.temp_day) + timedelta(days=1)
            new_day_of_year = self.get_day_of_year(new_date.year, new_date.month, new_date.day)
            dh = (new_day_of_year - 5) % 10
        else:
            day_of_year = self.get_day_of_year(self.year, self.month, self.day)
            dh = (day_of_year - 5) % 10
        self.he = round((self.hour * 60 + self.minute) / 120) + 1
        if self.he > 12:
            self.he = self.he % 12
        self.hh = (dh * 2 + self.he - 2) % 10
        if self.hh == 0:
            self.hh = 10
        # print(hh, he, end=' ')
        self.hour_word = EightWord.heaven[self.hh] + EightWord.earth[self.he]
        return self.hour_word


if __name__ == '__main__':
    y = 2023
    m = 3
    mi = 30
    for d in range(20, 29):
        for h in range(0, 24):
            e = EightWord(y, m, d, h, mi)
            print(f'{y}-{m}-{d} {h}:{mi} :', end=' ', )
            print(e.get_year_word(), end=' ')
            print(e.get_month_word(), end=' ')
            print(e.get_day_word(), end=' ')
            print(e.get_hour_word())

    y = 2023
    h = 12
    mi = 30
    for m in range(1, 3):
        for d in range(0, 29):
            e = EightWord(y, m, d, h, mi)
            print(f'{y}-{m}-{d} {h}:{mi} :', end=' ', )
            print(e.get_year_word(), end=' ')
            print(e.get_month_word(), end=' ')
            print(e.get_day_word(), end=' ')
            print(e.get_hour_word())

    h = 12
    mi = 30
    for y in range(2020, 2024):
        for m in range(1, 13):
            for d in [8, 28]:
                e = EightWord(y, m, d, h, mi)
                print(f'{y}-{m}-{d} {h}:{mi} :', end=' ', )
                print(e.get_year_word(), end=' ')
                print(e.get_month_word(), end=' ')
                print(e.get_day_word(), end=' ')
                print(e.get_hour_word())
