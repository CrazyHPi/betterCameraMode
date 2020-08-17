# -*- coding: utf-8 -*-

import re
import os
import time

def on_load(server, old):
    server.add_help_message('!!c', '更好的灵魂出窍/观察者摄像机')
    if not os.path.exists('./plugins/betterCameraMode/'):
        os.makedirs('./plugins/betterCameraMode/')

def on_info(server, info):
    #需要PlayerInfoAPI
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    if info.is_player and info.content == '!!c':
        result = PlayerInfoAPI.getPlayerInfo(server,info.player)
        #检查玩家游戏模式，只在生存下生效，本意是作为carpet的caramemode在生存里比较legit的实现
        if result['playerGameType'] == 1 :
            server.reply(info, '§4在？你为啥是创造模式？')
        elif result['playerGameType'] == 2 :
            server.reply(info, '§4在？你为啥是冒险模式？')
        elif result['playerGameType'] == 0 :
            with open('./plugins/betterCameraMode/' + info.player, 'w+') as f:
                f.write(
                    str(round(float(result["Pos"][0]),1)) + ' ' +
                    str(round(float(result["Pos"][1]),1)) + ' ' +
                    str(round(float(result["Pos"][2]),1)) + ' ' +
                    str(result["Dimension"]))
            server.reply(info, '§2位置已保存，灵魂出窍辣')
            server.reply(info, '§6使用!!c回到本体')
            server.execute('gamemode spectator ' + info.player)
        elif result['playerGameType'] == 3 :
            if os.path.exists('./plugins/betterCameraMode/' + info.player):
                with open('./plugins/betterCameraMode/'+ info.player, 'r') as f:
                    pos = f.read().split()
                if pos[3] == '0':
                    server.execute('execute in minecraft:overworld run tp ' + info.player + ' ' + pos[0] + ' ' + pos[1] + ' ' + pos[2])
                elif pos[3] == '-1':
                    server.execute('execute in minecraft:the_nether run tp ' + info.player + ' ' + pos[0] + ' ' + pos[1] + ' ' + pos[2])
                elif pos[3] == '1':
                    server.execute('execute in minecraft:the_end run tp ' + info.player + ' ' + pos[0] + ' ' + pos[1] + ' ' + pos[2])
                time.sleep(0.05)
                server.execute('gamemode survival ' + info.player)
                server.reply(info, '§2欢迎回来')
                os.remove('./plugins/betterCameraMode/'+ info.player)
            else:
                server.reply(info, '§4没找到你的本体，原地变身了')
                server.execute('gamemode survival ' + info.player)
