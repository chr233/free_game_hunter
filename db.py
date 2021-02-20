'''
# @Author       : Chr_
# @Date         : 2021-02-19 16:16:53
# @LastEditors  : Chr_
# @LastEditTime : 2021-02-20 13:46:22
# @Description  : 数据库api
'''

import sqlite3
from cfg import get_cfg


def get_conn():
    '''创建数据库连接'''
    db = get_cfg('db').get('db_name')
    try:
        conn = sqlite3.connect(db)
        return conn
    except Exception as e:
        print('创建数据库连接失败,请确保存在data.db文件')


def add_owned_game(cur: sqlite3.Cursor, bot: str, appids: list):
    '''添加拥有的游戏'''
    for app in appids:
        try:
            cur.execute(
                'INSERT INTO "owned"("appid","bot") VALUES (?,?)', (app, bot))
        except sqlite3.IntegrityError:
            print(f'数据已存在 {bot} - {app}')


def get_owned_game(cur: sqlite3.Cursor, bot: str, get_total: bool = False) -> list:
    '''获取已拥有的游戏'''
    cur.execute('SELECT COUNT(*) FROM "owned" WHERE bot=?', (bot,))
    total = cur.fetchone()[0]
    print(f'{bot} 已拥有 {total} 个免费游戏')

    if get_total:
        return total

    appids = []
    for i in range(0, total+1, 1000):
        cur.execute('SELECT "appid" FROM "owned" WHERE bot=? LIMIT ?,1000',
                    (bot, i))
        t = [x[0] for x in cur.fetchall()]
        appids.extend(t)
    return appids


def add_cache_game(cur: sqlite3.Cursor, appids: list):
    '''添加免费游戏缓存'''
    for app in appids:
        try:
            cur.execute('INSERT INTO "cache"("appid") VALUES (?)', (app, ))
        except sqlite3.IntegrityError:
            print(f'数据已存在 - {app}')


def get_cache_game(cur: sqlite3.Cursor, get_total: bool = False) -> list:
    '''获取免费游戏缓存'''
    cur.execute('SELECT COUNT(*) FROM "cache"')
    total = cur.fetchone()[0]
    print(f'缓存中共有 {total} 个免费游戏')

    if get_total:
        return total

    appids = []
    for i in range(0, total+1, 1000):
        cur.execute('SELECT "appid" FROM "cache" LIMIT ?,1000', (i,))
        t = [x[0] for x in cur.fetchall()]
        appids.extend(t)
    return appids


def get_status(cur: sqlite3.Cursor, name: str) -> int:
    '''获取status'''
    cur.execute('SELECT "value" FROM "status" WHERE "name"=?', (name,))
    t = cur.fetchone()
    return t[0] if t else 0


def set_status(cur: sqlite3.Cursor, name: str, value: int):
    '''更新status'''
    cur.execute('UPDATE "status" SET "value"=? WHERE "name"=?;', (value, name))


