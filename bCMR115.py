# -*- coding: utf-8 -*-

import re
import os
import time

bcmr_user = 0

def on_load(server, old):
    server.add_help_message('!!c', '更好的灵魂出窍/观察者摄像机')
    if not os.path.exists('./plugins/betterCameraMode/'):
        os.makedirs('./plugins/betterCameraMode/')

def process_coordinate(text):
    data = text[1:-1].replace('d', '').split(', ')
    data = [(x + 'E0').split('E') for x in data]
    return tuple([float(e[0]) * 10 ** int(e[1]) for e in data])

def change_mode(server, name, gm, dim, pos):
    if gm == '0':
        with open('./plugins/betterCameraMode/' + name, 'w+') as f:
            f.write(dim  + ' ' + str(round(pos[0],1)) + ' ' + str(round(pos[1],1)) + ' ' + str(round(pos[2],1)))
        server.tell(name, '§2位置已保存，灵魂出窍辣')
        server.tell(name, '§6使用!!c回到本体')
        server.execute('gamemode spectator ' + name)
    elif gm =='3':
        if os.path.exists('./plugins/betterCameraMode/' + name):
            with open('./plugins/betterCameraMode/'+ name, 'r') as f:
                pos = f.read().split()
            #server.execute('execute in ' + pos[0] + ' run tp ' + name + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3])
            if pos[0] == '0':
                server.execute('execute in minecraft:overworld run tp ' + name + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3])
            elif pos[0] == '-1':
                server.execute('execute in minecraft:the_nether run tp ' + name + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3])
            elif pos[0] == '1':
                server.execute('execute in minecraft:the_end run tp ' + name + ' ' + pos[1] + ' ' + pos[2] + ' ' + pos[3])
            time.sleep(0.05)
            server.execute('gamemode survival ' + name)
            server.tell(name, '§2欢迎回来')
            os.remove('./plugins/betterCameraMode/'+ name)
        else:
                server.tell(name, '§4没找到你的本体，原地变身了')
                server.execute('gamemode survival ' + name)

def on_info(server, info):
    if info.is_player and info.content == '!!c' or info.is_player and info.content == '!!C':
        global bcmr_user
        bcmr_user += 1
        server.execute('data get entity ' + info.player)
    if not info.is_player and bcmr_user > 0 and re.match(r'\w+ has the following entity data: ', info.content) is not None:
        name = info.content.split(' ')[0]
        gm = re.search(r'(?<= playerGameType: )(.*?),', info.content).group().replace(',','')
        dimension = re.search(r'(?<= Dimension: )(.*?),', info.content).group().replace('"', '').replace(',', '')
        position_str = re.search(r'(?<=Pos: )\[.*?\]', info.content).group()
        position = process_coordinate(position_str)
        change_mode(server, name, gm, dimension, position)
        bcmr_user -= 1
