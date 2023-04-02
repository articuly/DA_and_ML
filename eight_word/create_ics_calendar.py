from datetime import timedelta
import pandas as pd
from ics import Calendar, Event
from skyfield_datetime_util import convert_to_datetime

df = pd.read_csv('filter_eight_word.csv')
date_format = '%Y-%m-%d %H:%M:%S'
cal = Calendar()

for i, c in df.iterrows():
    dt = convert_to_datetime(c.datetime, to_utc=False, date_format=date_format)
    dt_begin = dt - timedelta(hours=0.5)
    dt_end = dt + timedelta(hours=0.5)
    print(dt_begin, dt_end)
    eight_word = c.eight_word

    e = Event(name=f'温暖之时：{eight_word}', begin=dt_begin, end=dt_end)
    cal.events.add(e)
    print(cal.events)

with open('my_eight_word.ics', 'w', encoding='utf-8') as my_file:
    my_file.writelines(cal.serialize_iter())
