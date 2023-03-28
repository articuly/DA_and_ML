from skyfield import api
from skyfield import almanac
from skyfield import almanac_east_asia
from datetime import datetime, timezone


def convert_to_datetime(datetime_str: str):
    # 将时间字符串转换为Python的datetime类型
    dt = datetime.strptime(datetime_str, '%Y%m%d %H%M%S')
    # 将datetime类型转换为UTC时区
    utc_dt = dt.astimezone(timezone.utc)
    return utc_dt


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
    utc_time = convert_to_datetime(datetime_str)
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
    utc_time = convert_to_datetime(datetime_str)
    ts = api.load.timescale()
    sky_utc_time = ts.utc(utc_time)
    terms_list = solar_terms_list(utc_time.year, ts)
    if sky_utc_time - terms_list[2][1] >= 0:
        is_after_spring_begin = True
    else:
        is_after_spring_begin = False
    return is_after_spring_begin


def list_solar_terms(year: int):
    ts = api.load.timescale()
    eph = api.load('de421.bsp')
    t0 = ts.utc(year, 1, 1)
    t1 = ts.utc(year, 12, 31)
    t, tm = almanac.find_discrete(t0, t1, almanac_east_asia.solar_terms(eph))
    for tmi, ti in zip(tm, t):
        print(tmi, almanac_east_asia.SOLAR_TERMS_ZHS[tmi], ti.utc_iso(' '))


if __name__ == '__main__':
    c = compare_solar_terms('20231208 120000')
    print(c)
    list_solar_terms(2023)
