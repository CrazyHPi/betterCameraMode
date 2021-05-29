# -*- coding: utf-8 -*-

import re
import os
import time

#==========使用者权限==========
# 0:guest 1:user 2:helper 3:admin 4:owner
bcmr_perm_lvl = 0
#==============================

bcmr_user = 0

def on_load(server, old):
    server.add_help_message('!!c', '灵魂出窍/观察者摄像机')
    if not os.path.exists('./plugins/betterCameraMode/'):
        os.makedirs('./plugins/betterCameraMode/')

def bcmr_process_coordinate(text):
    data = text[1:-1].replace('d', '').split(', ')
    data = [(x + 'E0').split('E') for x in data]
    return tuple([float(e[0]) * 10 ** int(e[1]) for e in data])

def bcmr_change_mode(server, name, gm, dim, pos):
    if gm == '0':
        with open('./plugins/betterCameraMode/' + name, 'w+') as f:
            f.write(dim  + ' ' + str(round(pos[0],2)) + ' ' + str(round(pos[1],2)) + ' ' + str(round(pos[2],2)))
        server.tell(name, '§2位置已保存，灵魂出窍辣')
        server.tell(name, '§6使用!!c回到本体')
        server.execute('gamemode spectator ' + name)
    elif gm =='3':
        if os.path.exists('./plugins/betterCameraMode/' + name):
            with open('./plugins/betterCameraMode/'+ name, 'r') as f:
                pos = f.read().split()
            server.execute('execute in ' + pos[0] + ' run tp ' + name + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3])
            time.sleep(0.05)
            server.execute('gamemode survival ' + name)
            server.execute('execute in ' + pos[0] + ' run tp ' + name + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3])
            server.tell(name, '§2欢迎回来')
            os.remove('./plugins/betterCameraMode/'+ name)
        else:
                server.tell(name, '§4没找到你的本体，原地变身了')
                server.execute('gamemode survival ' + name)

def on_user_info(server, info):
    if (info.content == '!!c' or info.content == '!!C' or info.content == '！！c' or info.content == '！！C'):
        if server.get_permission_level(info.player) >= bcmr_perm_lvl:
            global bcmr_user
            bcmr_user += 1
            server.execute('data get entity ' + info.player)
        else:
            server.tell(info.player, "§4权限不足")

def on_info(server, info):
    global bcmr_user
    if not info.is_player and bcmr_user > 0 and re.match(r'\w+ has the following entity data: ', info.content) is not None:
        name = info.content.split(' ')[0]
        gm = re.search(r'(?<= playerGameType: )(.*?),', info.content).group().replace(',','')
        if gm == '0' or gm == '3':
            dimension = re.search(r'(?<= Dimension: )(.*?),', info.content).group().replace('"', '').replace(',', '')
            position_str = re.search(r'(?<=Pos: )\[.*?\]', info.content).group()
            position = bcmr_process_coordinate(position_str)
            bcmr_change_mode(server, name, gm, dimension, position)
        bcmr_user -=1
