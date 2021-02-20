'''
# @Author       : Chr_
# @Date         : 2021-02-19 11:21:37
# @LastEditors  : Chr_
# @LastEditTime : 2021-02-20 14:18:53
# @Description  : ASF接口
'''

from typing import Tuple
from cfg import get_cfg
import asyncio
from ASF import IPC


def init_IPC():
    ASF_CFG = get_cfg('asf')
    addr = ASF_CFG.get('ipc_addr')
    passwd = ASF_CFG.get('ipc_password')

    return {'ipc': addr, 'password': passwd, 'timeout': 30}


async def exec_commend(ipc: IPC, cmd: str):
    '''执行命令'''
    for _ in range(3):
        resp = await ipc.Api.Command.post(body={'Command': cmd})
        if resp.success:
            return resp.result
        else:
            print(resp.message)


async def check_owned_game(bot: str, appids: list) -> Tuple[list, list]:
    '''检查是否已经拥有'''
    cfg = init_IPC()
    async with IPC(**cfg) as ipc:
        owned = []
        not_owned = []
        for app in appids:
            resp = await exec_commend(ipc, f'owns {bot} app/{app}')
            # print(resp)
            if '<ASF>' in resp or '已拥有' in resp:
                print(f'{bot} 已拥有 {app}')
                owned.append(app)
            else:
                print(f'{bot} 未拥有 {app}')
                not_owned.append(app)
                if len(not_owned) > 40 :
                    break
    return (owned, not_owned)


async def add_free_game(bot: str, appids: list) -> list:
    '''添加免费游戏'''
    cfg = init_IPC()
    async with IPC(**cfg) as ipc:
        added = []
        for app in appids:
            resp = await exec_commend(ipc, f'addlicense {bot} app/{app}')
            # print(resp)
            if 'sub/' in resp:
                print(f'{bot} 添加成功 {app}')
                added.append(app)
            else:
                print(f'{bot} 添加失败 {app}')
    return added


if __name__ == '__main__':
    async def main():
        await add_free_game('1', [123, 1329410, 730, 1402460])
    loop = asyncio.get_event_loop()
    output = loop.run_until_complete(main())
    loop.close()
