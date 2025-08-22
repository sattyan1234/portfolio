import pygame
from pygame.locals import *
import sys
import math
import time
#import asyncio
import graphics
import inputer

pygame.init()
#盤面の空白、白石、黒石の情報
state=[[0, 2, 2, 0, 0, 1, 1, 0],
       [2, 0, 0, 2, 1, 0, 0, 1],
       [2, 0, 0, 0, 0, 0, 0, 1],
       [2, 0, 0, 1, 2, 0, 0, 1],
       [2, 0, 0, 2, 1, 0, 0, 1],
       [0, 2, 0, 0, 0, 0, 1, 0],
       [0, 0, 2, 0, 0, 1, 0, 0],
       [0, 0, 0, 2, 1, 0, 0, 0]]
grid = [[0 for _ in range(8)] for _ in range(8)]  #0は空白,1は黒,2は白 
##初期配置（中央に4つの石を配置）
grid[3][3] = grid[4][4] = 2  #白石
grid[3][4] = grid[4][3] = 1  #黒石



current_turn = -1
situation= 0 #0:プレイ中１
Gra = graphics.Graphics()
Imp = inputer.Inputer()

Gra.window_clear()
Gra.board_update(state)
Gra.turnfinish = 1
running = True

while running:

    #タイマー
    if Gra.turnfinish == 1:
        current_turn = current_turn*(-1)#ターン切り替え今回は持ち時間が終わった瞬間に相手へ手番が移っている
        Gra.timer_set(Gra.fulltime, current_turn)




    # イベント処理
    for event in pygame.event.get():


        if event.type == Gra.countdown:#カウントダウン用のイベントが発生したら更新
            Gra.timer_update()
        if event.type == Gra.pop_invalid_delete:
            Gra.pop_delete()

        #クリックされたら
        if event.type == MOUSEBUTTONDOWN:
            print(Imp.boardclickwhere(event.pos, event.button))#クリックの情報をターミナル？にプリント
            if Imp.boardclickwhere(event.pos, event.button)[0] == "surrender":#降参が押されたとき
                Gra.pop_surrender()#降参pop表示
                situation = 1#降参popの状態へ遷移
                break
            elif Imp.boardclickwhere(event.pos, event.button)[0] == "board":
                print(Imp.boardclickwhere(event.pos, event.button)[1])
                if Imp.boardclickwhere(event.pos, event.button)[1] == (0,0):
                    Gra.pop_invalid()
            


        #windowを×などで消す用
        if event.type == QUIT: 
            running = False
            pygame.quit()#ウィンドウ消す
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:   
                running = False
                pygame.quit()#ウィンドウ消す
    
    while situation == 1:#降参popの状態
        #イベント処理
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                print(Imp.decision_surrender(event.pos, event.button))#押されたボタンをターミナル？にプリント
                if Imp.decision_surrender(event.pos, event.button) == "yes":#yesなら勝敗pop表示
                    Gra.pop_conclusion(2, 10, 15)
                    situation = 2
                    break

                elif Imp.decision_surrender(event.pos, event.button) == "no":#noなら再開
                    situation = 0#状態をプレイ中に遷移
                    Gra.window_clear()
                    Gra.board_update(state)
                    break
            
            #windowを×などで消す用
            if event.type == QUIT: 
                running = False
                situation = 0
                pygame.quit()#ウィンドウ消す
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   
                    running = False
                    situation = 0
                    pygame.quit()#ウィンドウ消す
                    break
    while situation == 2:#勝敗ポップの状態
        #イベント処理
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                print(Imp.decision_continue(event.pos, event.button))#押されたボタンをターミナル？にプリント
                if Imp.decision_continue(event.pos, event.button) == "again":
                    #初期化
                    situation = 0#状態をプレイ中に遷移
                    Gra.turnfinish = 0
                    current_turn = 1
                    Gra.timer_set(Gra.fulltime,current_turn)
                    Gra.window_clear()
                    Gra.board_update(grid)
                    break
                if Imp.decision_continue(event.pos, event.button) == "end":
                    running = False
                    situation = 0
                    time.sleep(2)
                    pygame.quit()#ウィンドウ消す
                    break
            #windowを×などで消す用
            if event.type == QUIT: 
                running = False
                situation = 0
                pygame.quit()#ウィンドウ消す
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   
                    running = False
                    situation = 0
                    pygame.quit()#ウィンドウ消す
                    break