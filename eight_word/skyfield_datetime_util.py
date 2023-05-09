from datetime import datetime, timezone, date
from pytz import timezone as tz
from skyfield import almanac
from skyfield import almanac_east_asia
from skyfield import api
import time


def convert_to_datetime(datetime_str: str, to_utc=False, date_format='%Y%m%d %H%M%S'):
    # 将时间字符串转换为Python的datetime类型
    dt = datetime.strptime(datetime_str, date_format)
    if to_utc:
        return dt.astimezone(timezone.utc)
    else:
        return dt.astimezone(tz('Asia/Shanghai'))


def datetime_returns(year_to_day: str, hour_to_second: str):
    # 将字符串返回成多个时间变量
    dt = convert_to_datetime(year_to_day + ' ' + hour_to_second, to_utc=False)
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second


def get_day_of_year(year, month, day):
    # 获取一年中的第几天
    the_date = date(year, month, day)
    day_of_year = int(the_date.strftime('%j'))
    return day_of_year


def solar_terms_list(year: int, ts):
    # 加载天文历
    eph = api.load('de421.bsp')
    # 加载Skyfield时间刻度
    start_time = ts.utc(year, 1, 1)
    end_time = ts.utc(year, 12, 31)
    # 获取节气信息
    time, enum = almanac.find_discrete(start_time, end_time, almanac_east_asia.solar_terms(eph))
    return list(zip(enum, time))


def compare_solar_terms(datetime_str: str):
    # 将时间字符串对比节气，返回时间的节气索引
    utc_time = convert_to_datetime(datetime_str, to_utc=False)
    ts = api.load.timescale()
    sky_utc_time = ts.utc(utc_time)
    terms_list = solar_terms_list(utc_time.year, ts)
    list_len = len(terms_list)
    num = -1
    for i in range(0, list_len - 1):
        if sky_utc_time - terms_list[0][1] < 0:
            num = terms_list[0][0] - 1
        elif sky_utc_time - terms_list[list_len - 1][1] >= 0:
            num = terms_list[list_len - 1][0]
        elif sky_utc_time - terms_list[i][1] >= 0 and sky_utc_time - terms_list[i + 1][1] < 0:
            num = terms_list[i][0]
    return num


def compare_spring_begin(datetime_str: str):
    # 将时间字符串对比今年的立春节气
    utc_time = convert_to_datetime(datetime_str, to_utc=False)
    ts = api.load.timescale()
    sky_utc_time = ts.utc(utc_time)
    terms_list = solar_terms_list(utc_time.year, ts)
    if sky_utc_time - terms_list[2][1] >= 0:
        is_after_spring_begin = True
    else:
        is_after_spring_begin = False
    return is_after_spring_begin


def list_solar_terms(year: int):
    # 显示某年的节气时间信息
    ts = api.load.timescale()
    eph = api.load('de421.bsp')
    t0 = ts.utc(year, 1, 1)
    t1 = ts.utc(year, 12, 31)
    t, tm = almanac.find_discrete(t0, t1, almanac_east_asia.solar_terms(eph))
    for tmi, ti in zip(tm, t):
        print(tmi, almanac_east_asia.SOLAR_TERMS_ZHS[tmi], ti.utc_iso(' '))


if __name__ == '__main__':
    start_time = datetime.now()
    c = compare_spring_begin('20230101 033000')
    print(c)
    d = compare_solar_terms('20230701 123000')
    print(d)
    end_time = datetime.now()
    print(end_time-start_time)
    # list_solar_terms(2023)
    # d = convert_to_datetime('20230101 033000', to_utc=True)
    # print(d)