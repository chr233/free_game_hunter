'''
# @Author       : Chr_
# @Date         : 2021-02-19 12:11:05
# @LastEditors  : Chr_
# @LastEditTime : 2021-02-20 23:20:59
# @Description  : 存取设置
'''

import toml
import os

CFG = {}
loaded = False


def load_cfg():
    '''读取设置'''
    def parse_bot(r: dict) -> dict:
        bots = r.get('bot_name')
        if isinstance(bots, str):
            bots = [bots]
        vbots = []
        for bot in bots:
            if str(bot).lower() != 'asf':
                vbots.append(bot)
        if len(vbots) == 0:
            raise ValueError('尚未配置任何机器人')
        return {'bot_name': vbots}

    def parse_asf(r: dict) -> dict:
        addr = r.get('ipc_addr')
        passwd = r.get('ipc_password')
        return {'ipc_addr': addr, 'ipc_password': passwd}

    def parse_db(r: dict) -> dict:
        name = r.get('db_name')
        return {'db_name': name}

    with open('config.toml', 'r', encoding='utf-8') as f:
        raw_cfg = toml.load(f)
    global CFG
    CFG = {
        'bot': parse_bot(raw_cfg.get('bot', {})),
        'asf': parse_asf(raw_cfg.get('asf', {})),
        'db': parse_db(raw_cfg.get('db', {}))
    }
    global loaded
    loaded = True


def get_cfg(name: str = None) -> dict:
    '''获取设置'''
    if not loaded:
        raise ValueError('未初始化')
    return CFG.get(name) if name else CFG


load_cfg()
print(CFG)
