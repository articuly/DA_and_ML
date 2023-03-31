# coding: utf-8
from datetime import datetime, timedelta, date
import csv
from skyfield_solar_terms import compare_solar_terms, compare_spring_begin, convert_to_datetime


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
        self.datetime_str = f'{self.year}{self.month:0>2d}{self.day:0>2d} {self.hour:0>2d}{self.minute:0>2d}{self.second:0>2d}'
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

    def get_solar_terms_index(self):
        solar_term_index = compare_solar_terms(self.datetime_str)
        return solar_term_index

    def test_spring_begin(self):
        is_after_spring_begin = compare_spring_begin(self.datetime_str)
        return is_after_spring_begin

    def get_year_word(self):
        if self.year < 2000:
            print('年份错误，请输入2000年后的八字')
        else:
            self.yh = (self.year - 3) % 10 or 10
            self.ye = (self.year - 3) % 12
            if (not self.test_spring_begin()) or (self.month == 1 and self.day == 1):
                self.yh = self.yh - 1
                if self.yh < 1:
                    self.yh = 10
                self.ye = self.ye - 1
                if self.ye < 1:
                    self.ye = 12
            # print(self.yh, self.ye, end=' ')
            self.year_word = EightWord.heaven[self.yh] + EightWord.earth[self.ye]
            return self.year_word

    def get_month_word(self):
        st_idx = self.get_solar_terms_index()
        self.me = (st_idx + 1) // 2 + 4
        if self.me > 12:
            self.me = self.me - 12

        if st_idx == 18 and self.month == 1:
            local_year = self.year - 1
        else:
            local_year = self.year
        local_yh = (local_year - 3) % 10 or 10
        local_me = self.me
        if self.me == 1:
            local_me = 13
        self.mh = (local_yh * 2 + local_me - 2) % 10 or 10
        # print(self.mh, self.me, end=' ')
        self.month_word = EightWord.heaven[self.mh] + EightWord.earth[self.me]
        return self.month_word

    def get_day_word(self):
        day_of_year = self.get_day_of_year(self.year, self.month, self.day)
        self.dh = (day_of_year - 5) % 10 or 10
        self.de = (day_of_year - 5) % 12 or 12
        # print(self.dh, self.de, end=' ')
        self.day_word = EightWord.heaven[self.dh] + EightWord.earth[self.de]
        return self.day_word

    def get_hour_word(self):
        if self.hour >= 23:
            new_date = date(self.year, self.month, self.day) + timedelta(days=1)
            day_of_year = self.get_day_of_year(new_date.year, new_date.month, new_date.day)
        else:
            day_of_year = self.get_day_of_year(self.year, self.month, self.day)

        local_dh = (day_of_year - 5) % 10
        self.he = round((self.hour * 60 + self.minute) / 120) + 1
        if self.he > 12:
            self.he = self.he % 12
        self.hh = (local_dh * 2 + self.he - 2) % 10
        if self.hh == 0:
            self.hh = 10
        # print(self.hh, self.he, end=' ')
        self.hour_word = EightWord.heaven[self.hh] + EightWord.earth[self.he]
        return self.hour_word

    def get_datetime_str(self):
        return f'{self.year}-{self.month:0>2d}-{self.day:0>2d} {self.hour:0>2d}:{self.minute:0>2d}:{self.second:0>2d}'


if __name__ == '__main__':
    # Test 1
    # y = 2023
    # m = 3
    # mi = 30
    # for d in range(20, 29):
    #     for h in range(0, 24):
    #         e = EightWord(y, m, d, h, mi)
    #         print(f'{y}-{m}-{d} {h}:{mi} ->', end=' ', )
    #         print(e.get_year_word(), end=' ')
    #         print(e.get_month_word(), end=' ')
    #         print(e.get_day_word(), end=' ')
    #         print(e.get_hour_word())

    # Test 2
    # y = 2023
    # h = 12
    # mi = 30
    # for m in range(1, 3):
    #     for d in range(1, 29):
    #         e = EightWord(y, m, d, h, mi)
    #         print(f'{y}-{m}-{d} {h}:{mi} ->', end=' ', )
    #         print(e.get_year_word(), end=' ')
    #         print(e.get_month_word(), end=' ')
    #         print(e.get_day_word(), end=' ')
    #         print(e.get_hour_word())

    # Test 3
    # h = 12
    # mi = 30
    # for y in range(2021, 2024):
    #     for m in range(1, 13):
    #         for d in [8, 28]:
    #             e = EightWord(y, m, d, h, mi)
    #             print(f'{y}-{m}-{d} {h}:{mi} ->', end=' ', )
    #             print(e.get_year_word(), end=' ')
    #             print(e.get_month_word(), end=' ')
    #             print(e.get_day_word(), end=' ')
    #             print(e.get_hour_word())

    # test 4
    mi = 30
    for y, m in [(2022, 12), (2023, 1), (2023, 2)]:
        for d in range(1, 32):
            for h in [0, 12, 23]:
                try:
                    datetime(y, m, d, h, mi)
                except Exception:
                    continue
                else:
                    e = EightWord(y, m, d, h, mi)
                    print(f'{y}-{m}-{d} {h}:{mi} ->', end=' ', )
                    print(e.get_year_word(), end=' ')
                    print(e.get_month_word(), end=' ')
                    print(e.get_day_word(), end=' ')
                    print(e.get_hour_word())

    # start_time = datetime(2023, 1, 1, 0, 30)
    # end_time = datetime(2025, 12, 31, 23, 59)
    # delta = timedelta(hours=1)
    # header = ['datetime', 'year', 'month', 'day', 'hour', 'minute',
    #           'year_word', 'month_word', 'day_word', 'hour_word', 'eight_word']
    #
    # time_list = []
    # while start_time <= end_time:
    #     time_list.append(start_time)
    #     start_time += delta
    #
    # with open('eight_word.csv', mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(header)
    #     for t in time_list:
    #         y, m, d, h, mi = t.year, t.month, t.day, t.hour, t.minute
    #         print(f'{y}-{m}-{d} {h}:{mi}:00')
    #         e = EightWord(y, m, d, h, mi)
    #         ew = e.get_year_word() + e.get_month_word() + e.get_day_word() + e.get_hour_word()
    #         row = [e.get_datetime_str(), y, m, d, h, mi, e.get_year_word(), e.get_month_word(), e.get_day_word(),
    #                e.get_hour_word(), ew]
    #         writer.writerow(row)
