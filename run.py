'''
# @Author       : Chr_
# @Date         : 2021-02-19 11:13:57
# @LastEditors  : Chr_
# @LastEditTime : 2021-03-05 14:04:48
# @Description  : 启动入口
'''

import asyncio
import traceback
from time import time
from cfg import get_cfg
import db
import steam
import asf_api


def check_appids(A: list, B: list) -> list:
    '''返回A和B的补集的交集'''
    C = [x for x in A if x not in B]
    return C


def remove_duplicate(A: list) -> list:
    '''列表去重'''
    C = list(set(A))
    return C


def check_cache(conn: db.sqlite3.Connection):
    '''检查缓存,判断是否需要更新'''
    cur = conn.cursor()

    duplicate = db.get_status(cur, 'duplicate')
    cache_total = db.get_cache_game(cur, True)
    store_total = steam.get_free_games(True)

    update_time = db.get_status(cur, 'update')
    curr_time = int(time())

    flag = curr_time - update_time > 604800 or abs(store_total - cache_total - duplicate) > 10

    print('需要更新缓存' if flag else '无需更新缓存')
    return flag


async def process_bot(conn: db.sqlite3.Connection, bot: str, free_game: list):
    '''处理每个机器人的任务'''
    cur = conn.cursor()
    db_owned = db.get_owned_game(cur, bot)
    cur.close()

    not_owned = check_appids(free_game, db_owned)
    v_owned, v_not_owned = await asf_api.check_owned_game(bot, not_owned)
    cur = conn.cursor()
    db.add_owned_game(cur, bot, v_owned)
    conn.commit()
    cur.close()

    await asf_api.add_free_game(bot, v_not_owned)
    succ_owned, _ = await asf_api.check_owned_game(bot, v_not_owned)
    cur = conn.cursor()
    db.add_owned_game(cur, bot, succ_owned)
    count = db.get_status(cur, 'added')
    db.set_status(cur, 'added', count + len(succ_owned))
    conn.commit()
    cur.close()


async def main():
    '''主程序'''
    try:
        conn = db.get_conn()
    
        if check_cache(conn):
            print('即将更新缓存,速度较慢,请耐心等待')
            free_game = steam.get_free_games(False)
            free_game_d = remove_duplicate(free_game)
            duplicate = len(free_game)-len(free_game_d)
            print(f'共有 {duplicate} 个重复的游戏')

            cur=conn.cursor()
            db.reset_cache_game(cur)
            conn.commit()
            cur=conn.cursor()
            db.add_cache_game(cur, free_game_d)
            conn.commit()
            cur=conn.cursor()
            db.set_status(cur, 'update', int(time()))
            db.set_status(cur, 'duplicate', duplicate)
            conn.commit()
            print('缓存更新完成')
        else:
            print('使用缓存数据')
            
            cur = conn.cursor()
            free_game = db.get_cache_game(cur, False)
        cur.close()

        bots = get_cfg('bot')['bot_name']
        for i, bot in enumerate(bots, 1):
            print(f'进度{i}/{len(bots)} 机器人 {bot}')
            await process_bot(conn, bot, free_game)

        cur = conn.cursor()
        count = db.get_status(cur, 'added')
        cur.close()
        conn.close()
        print(f'总计添加 {count} 个免费游戏')
        print('运行结束')
    except Exception as e:
        print('运行出错')
        print(e)
        traceback.print_stack()
        input('按回车键退出……')

loop = asyncio.get_event_loop()
output = loop.run_until_complete(main())
loop.close()
