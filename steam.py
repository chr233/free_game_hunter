'''
# @Author       : Chr_
# @Date         : 2021-02-19 12:11:14
# @LastEditors  : Chr_
# @LastEditTime : 2021-03-05 13:41:41
# @Description  : Steam商店API
'''
import re
import requests
from time import sleep
from static import HEADERS


def get_free_games(get_total:bool =False) -> list:
    ss = requests.Session()
    ss.headers = HEADERS

    def get_store_page(start: int = 0):
        '''获取商店单页内容'''
        url = f'https://store.steampowered.com/search/results/?query&start={start}&count=50&dynamic_data=&sort_by=_ASC&maxprice=free&category1=998&infinite=1'
        resp = ss.get(url=url, headers=HEADERS)
        for _ in range(3):
            try:
                return resp.json()
            except Exception as e:
                sleep(2)
                print(e)
        return {}

    def parse_html(html: str) -> list:
        '''分析html,返回appid列表'''
        s = re.findall(r'data-ds-appid="(\d+)"', html, re.MULTILINE)
        i = [int(x) for x in s]
        return i

    j = get_store_page(0)
    total = j.get('total_count', 0)
    print(f'商店共有 {total} 个免费游戏')

    if get_total:
        return total

    appids = []
    for i in range(0, total, 50):
        print(f'正在拉取第{i//50+1}页,{i} - {i+50}')
        j = get_store_page(i)
        h = j.get('results_html', '')
        if not h:
            continue
        a = parse_html(h)
        appids.extend(a)
    print(f'处理完成,共{len(appids)}个免费游戏')
    return appids

