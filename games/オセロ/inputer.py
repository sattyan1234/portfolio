
#盤面のクリックされた行列座標の出力、降参ボタンの押下の出力、降参の再確認状態でのyes/noの出力
import graphics
import pygame
from pygame.locals import *
import math
import sys
class Inputer:
    def __init__(self):
        #マウスのクリック当たり判定分割
        self.cdn = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                self.cdn[i][j]=pygame.Rect(i*78+2,j*78+2,75,75)
        #降参再確認ポップのyes/no当たり判定
        self.pop_surrender_yes = pygame.Rect(graphics.Graphics.pop_surrender_yes)
        self.pop_surrender_no = pygame.Rect(graphics.Graphics.pop_surrender_no)
    def boardclickwhere(self, event_pos, event_button, state, gra):#通常状態において、クリックされた行列座標の位置または降参ボタンが押されたかを返す
        cursor_x,cursor_y = event_pos
        #クリックがboard上のとき
        if event_button == 1 and cursor_x <= 78*8-1:
            cursor_mat_x = math.floor(cursor_x/78)#カーソルの座標を0~7までに振り分け
            cursor_mat_y = math.floor(cursor_y/78)
            #カーソルのあるであろう場所の周囲９マスと当たり判定
            for i in range(3):
                for j in range(3):
                    zero_x = zero_y = 1
                    if cursor_mat_x == 0 and i-1 <0:
                        zero_x = 0
                    else:
                        zero_x = 1
                    if cursor_mat_x == 7 and i-1 >0:
                        zero_x = 0
                    else:
                        zero_x = 1
                    if cursor_mat_y == 0 and j-1 <0:
                        zero_y = 0
                    else:
                        zero_y = 1
                    if cursor_mat_y == 7 and j-1 >0:
                        zero_y = 0
                    else:
                        zero_y = 1

                    if self.cdn[(i-1)*zero_x+cursor_mat_x][(j-1)*zero_y+cursor_mat_y].collidepoint(event_pos):
                        return ("board", ((j-1)*zero_y+cursor_mat_y,(i-1)*zero_x+cursor_mat_x))#(クリックされた行列座標,"board")を返す
        #ボタン上でクリックされたとき
        for button in gra.list_button[state]:
            if event_button == 1 and gra.button_rect[button].collidepoint(event_pos):
                return (button,False)#pauseをかえす
        return ("None", False)
    

    
    def pop_lr_click(self, event_pos):#ボタン付きポップのボタン入力チェック
        if (pygame.Rect(graphics.Graphics.pop_surrender_yes)).collidepoint(event_pos):
            return "leftbutton"
        if (pygame.Rect(graphics.Graphics.pop_surrender_no)).collidepoint(event_pos):
            return "rightbutton"
        return None
        

