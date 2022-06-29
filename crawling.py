'''
By Minsang Yu. flowerk94@gmail.com.
'''

import os
import datetime
import pandas as pd
from query_crawler import crawl
from itertools import repeat


def read_name_and_date(mode):
    if mode == 'listed':
        df = pd.read_excel('src/listed_list_2020.08.03.xlsx')
        names = df['회사명']
        dates = df['상장일']

        begins = [date.to_pydatetime() for date in dates.tolist()]
        ends = repeat(datetime.datetime.now())

    else:
        df = pd.read_excel('src/delisted_list_2010.01.01-2020.06.25.xlsx')
        df = df[~df['폐지사유'].isin(['코스닥시장 이전상장', '코스닥시장 상장', '유가증권시장 상장', '완전자회사화'])]
        names = df['회사명']
        dates = df['폐지일자']

        begins = repeat(datetime.datetime(2010, 1, 1))
        ends = [date.to_pydatetime() for date in dates.tolist()]

    return names, begins, ends


def crawl_query_by_month(query, begin, end, save_dir):
    print('\n====== DATA INFO ======')
    print('time:', datetime.datetime.now())
    print('name:', query)
    print('begin:', begin)
    print('end:', end)

    while end > begin:
        first_day = end.replace(day=1).strftime('%Y.%m.%d')
        last_day = end.strftime('%Y.%m.%d')

        print('\nstart crawling: %s from %s to %s' % (query, first_day, last_day))
        save_as = os.path.join(save_dir, query, query + '_' + first_day + '-' + last_day + '.xlsx')

        if os.path.exists(save_as):
            print('\talready crawled. go to next step')
        else:
            crawl(query, first_day, last_day, save_as)

        # go to last month
        end = end.replace(day=1) - datetime.timedelta(days=1)


def run(mode, period_days=0):
    names, begins, ends = read_name_and_date(mode)
    save_dir = 'data/crawled/' + mode

    for i, (name, begin, end) in enumerate(zip(names, begins, ends)):
        print(i, len(names))

        if period_days:
            begin = end - datetime.timedelta(days=period_days)

        try:
            os.makedirs(os.path.join(save_dir, name), exist_ok=True)
        except OSError as e:
            print('(ERROR!) illegal path,', e)
            continue

        crawl_query_by_month(name, begin, end, save_dir)


if __name__ == '__main__':
    run(mode='listed')
    run(mode='delisted')

