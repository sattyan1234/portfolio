#盤面の描画、駒配置の更新、時間タイマーセット、タイマーの数字更新、勝敗メッセージの表示、降参ボタンの表示
import pygame
from pygame.locals import *
import time
import asyncio
from ai import AI 

class Graphics(pygame.sprite.Sprite):
    #降参ボタンの当たり判定用データ(imputerで使う)
    btn_surrender = pygame.Rect(700,400,200,200)#降参ボタンの領域
    btn_surrender.centerx = 78*8+(1000-78*8)/2
    pop_surrender_bg = ((78*8)/2-200,78*8-550,400,500)
    pop_surrender_yes = (pop_surrender_bg[0]+10, 78*8-50-10-180, 180,180)
    pop_surrender_no = (pop_surrender_bg[0]+400-180-10, 78*8-50-10-180, 180,180)
    text_pop_invalid = "You can't put there ."#無効ポップのメッセージ
    text_pop_surrender = "Do you really want to give in ?"#降参ポップのメッセージ
    text_pop_pass = "pass"#ぱすポップのメッセージ
    pop_pass_delete = pygame.USEREVENT+1
    windowsize_x = 1000#ウィンドウのサイズ
    windowsize_y = 78*8
    white_img_pth = "画像2.png"#白石、黒石のパス
    black_img_pth = "画像1.png"
    stnsize = 60#駒のサイズ
    fulltime = 30#手番側の最初の持ち時間
    def __init__(self):#ここでウィンドウを作成
        pygame.font.init()
        self.screen = 0#使用するスクリーン用変数
        self.image = [[0 for _ in range(8)]for _ in range(8)]#駒用の配列
        self.state = [[0 for _ in range(8)]for _ in range(8)]
        self.font = pygame.font.Font(None, 80)#フォントとサイズ
        self.turnfinish = 0#誰かの手番のとき０，手番が終わった時１
        self.current_turn = 1#ターンを示す変数1:黒-1:白  current_turnで把握
        self.time = self.fulltime#カウントダウンの数字用変数
        self.timer_white = (78*8+(Graphics.windowsize_x-78*8)/2-15-130,55,130,180)#持ち時間ウィンドウの左上座標,幅、高さ
        self.timer_black = (78*8+(Graphics.windowsize_x-78*8)/2+15,55,130,180)
        self.timer_white_rect = pygame.Rect(78*8+(Graphics.windowsize_x-78*8)/2-15-130,55,130,180)#持ち時間ウィンドウの左上座標,幅、高さ
        self.timer_black_rect = pygame.Rect(78*8+(Graphics.windowsize_x-78*8)/2+15,55,130,180)
#        self.text_pop_surrender = "Do you really want to give in ?"#降参ポップのメッセージ
#        self.text_pop_surrender_image = pygame.transform.scale(self.font.render(self.text_pop_surrender, True, (255, 255, 255)), (Graphics.pop_surrender_bg[2],60))#降参ポップの画像作成、サイズ調整
        self.text_pop_pass_image = pygame.transform.scale(self.font.render(Graphics.text_pop_pass, True, (255, 255, 255)), (200,80))#ぱすポップの画像作成、サイズ調整
        self.text_pop_pass_rect = self.text_pop_pass_image.get_rect()
        self.text_pop_pass_rect.center = (Graphics.pop_surrender_bg[0]+Graphics.pop_surrender_bg[2]/2, Graphics.pop_surrender_bg[1]+Graphics.pop_surrender_bg[3]/2)
#        self.text_pop_invalid = "You can't put there ."#無効ポップのメッセージ
 #       self.text_pop_invalid_image = pygame.transform.scale(self.font.render(self.text_pop_invalid, True, (255, 255, 255)), (Graphics.pop_surrender_bg[2],60))#無効ポップの画像作成、サイズ調整
        #ウィンドウを作成
        self.screen = pygame.display.set_mode((Graphics.windowsize_x, Graphics.windowsize_y))#ウィンドウ作成
        pygame.display.set_caption("オセロゲーム")# 画面上部に表示するタイトル
        self.window_rect = {"a":1}
        self.button_rect = {"a":1}
        self.pop_on_board_bg = pygame.Rect(Graphics.pop_surrender_bg)
        self.pop_on_board_leftbutton = pygame.Rect(Graphics.pop_surrender_yes)
        self.pop_on_board_rightbutton = pygame.Rect(Graphics.pop_surrender_no)
        self.pop_on_board_lb_rect = {"a":1}
        self.pop_on_board_rb_rect = {"a":1}
        self.line = {"a":1}
        self.text_l = [0 for _ in range(10)]
        self.text_l_rect = [0 for _ in range(10)]
        self.text_b = [0 for _ in range(10)]
        self.text_b_rect = [0 for _ in range(10)]
        self.button = [0,0]
        self.list_button = [set(), set(),set()]#0:startmenu,1:play中,2:pop


    def window_clear(self, current_turn, player_type):#画面消去（黒塗り）からのオセロ盤の描画,タイマー再開(一番最初と、中断から再開する際に実行する)
        self.current_turn = current_turn
        self.screen.fill((0, 0, 0))#画面全体を黒で塗りつぶす
        #緑色の盤面を描画
        pygame.draw.rect(self.screen, (100,255,100), (0,0,78*8,78*8))
        #盤面のgridを描画
        for i in range(7):
            pygame.draw.line(self.screen, (100,100,200), (78*(i+1),0), (78*(i+1),78*8),3)
        for i in range(7):
            pygame.draw.line(self.screen, (100,100,200), (0,78*(i+1)), (78*8,78*(i+1)),3)
        #タイマーのもろもろ描画
        pygame.draw.rect(self.screen, (255,255,255), self.timer_white, 5)
        pygame.draw.line(self.screen, (255,255,255), (self.timer_white[0],self.timer_white[1]+50), (self.timer_white[0]+129,self.timer_white[1]+50), 5)
        pygame.draw.rect(self.screen, (100,100,255), self.timer_black, 5)
        pygame.draw.line(self.screen, (100,100,255), (self.timer_black[0],self.timer_black[1]+50), (self.timer_black[0]+129,self.timer_black[1]+50), 5)
        self.screen.blit(pygame.transform.scale(self.font.render("WHITE", True, (255, 255, 255)), (90,50)), (self.timer_white[0]+5,self.timer_white[1]+5))
        self.screen.blit(pygame.transform.scale(self.font.render("BLACK", True, (100, 100, 255)), (90,50)), (self.timer_black[0]+5,self.timer_black[1]+5))
        #現在の秒数でタイマーの数字描画（中断からの再開にも対応）
        text_time = self.font.render(str(self.time), True, (255, 255, 255))#持ち時間の画像
        text_time = pygame.transform.scale(text_time, (60, 60))#サイズ調整
        if self.current_turn == 1:#黒の手番のときのタイム
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_white[0]+130-30,self.timer_white[1]+25, 20,20))
            self.screen.blit(pygame.transform.scale(self.font.render("@", True, (100, 100, 255)), (20,20)), (self.timer_black[0]+130-30,self.timer_black[1]+25))
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_black[0]+35,self.timer_black[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(text_time, (self.timer_black[0]+35,self.timer_black[1]+85))#数字の描画
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_white[0]+35,self.timer_white[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(pygame.transform.scale(self.font.render("0", True, (255, 255, 255)), (60,60)), (self.timer_white[0]+35,self.timer_white[1]+85))#数字の描画
        else:#白の手番のときのタイム
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_black[0]+130-30,self.timer_black[1]+25, 20,20))
            self.screen.blit(pygame.transform.scale(self.font.render("@", True, (255, 255, 255)), (20,20)), (self.timer_white[0]+130-30,self.timer_white[1]+25))
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_white[0]+35,self.timer_white[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(text_time, (self.timer_white[0]+35,self.timer_white[1]+85))#数字の描画
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_black[0]+35,self.timer_black[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(pygame.transform.scale(self.font.render("0", True, (255, 255, 255)), (60,60)), (self.timer_black[0]+35,self.timer_black[1]+85))#数字の描画
        
        #aiの手番表示
        if player_type == 1 or player_type == 3:
            self.draw_on_window("<ai>", (self.timer_black_rect.centerx, self.timer_black_rect.top-20, 60, 30), (100,100,255))
        if player_type == 2 or player_type == 3:
            self.draw_on_window("<ai>", (self.timer_white_rect.centerx, self.timer_white_rect.top-20, 60, 30), (255,255,255))

        
        
        #pauseボタン
        self.make_button(1,"pause", 78*8+(1000-78*8)/2, 78*4+39, (1000-78*8)-20, 75) 

        if player_type == 3:#ai vs aiなら降参を表示しない
            return

        #降参ボタンの描画
        self.make_button(1, "surrender", self.btn_surrender.centerx, self.btn_surrender.centery, self.btn_surrender.width, self.btn_surrender.height)

        #画面への反映
  #      pygame.display.update()

    def start(self):#スタートメニュー作成
        self.make_window("start", 50)

        self.make_button(0, "with friend", 200, 400, 200, 200)
        self.make_button(0, "with ai", 500, 400, 200, 200)
        self.make_button(0, "watch", 800, 400, 200, 200)
        self.make_button(0, "end", Graphics.windowsize_x/2, (300+188)/2, 78, 78)
        self.draw_on_window("choose how you play", (500, 160, 0, 0), (255,255,255))


        #画面への反映
        pygame.display.update()
    
    def make_window(self, name, l):
        self.window_rect[name] = pygame.Rect(l, l, Graphics.windowsize_x - 2*l, Graphics.windowsize_y - 2*l)
        pygame.draw.rect(self.screen, (0,0,0), self.window_rect[name])
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(l+15, l+15, Graphics.windowsize_x - 2*l - 30, Graphics.windowsize_y - 2*l- 30), 5)
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(l, l, Graphics.windowsize_x - 2*l, Graphics.windowsize_y - 2*l), 5)

    
    def make_button(self, state, name, center_x, center_y, w, h):#state...0:startmenu,1:play中,2:pop
        self.list_button[state].add(name)
        self.button_rect[name] = pygame.Rect(center_x - w/2, center_y - h/2, w, h)
        pygame.draw.rect(self.screen, (0,150,0), self.button_rect[name])
        text = self.font.render(name, True, (255,255,255))
        text_rect = text.get_rect()
        if text_rect.width > w:
            text = pygame.transform.scale(text, (w, text_rect.height))
        if text_rect.height > h:
            text = pygame.transform.scale(text, (text_rect.width, h))
        text_rect = text.get_rect()
        text_rect.center = (center_x, center_y)
        self.screen.blit(text, text_rect)


    def board_update(self, state):#駒配置の更新（盤面状況のデータを受け取って駒の画像更新と表示）
        self.state = state
        #各マスの情報から駒の画像を配列に入れて、描画
        for row in range(8):
            for column in range(8):
                if state[row][column] == 0:
                    self.image[row][column] = pygame.image.load(Graphics.white_img_pth).convert_alpha()#駒の置かれてない部分は白石の画像を与えて、場外に表示させて隠す
                    bye=1#空白判定用
                elif state[row][column] == 1:
                    self.image[row][column] = pygame.image.load(Graphics.black_img_pth).convert_alpha()
                    bye=0
                elif state[row][column] == 2:
                    self.image[row][column] = pygame.image.load(Graphics.white_img_pth).convert_alpha()
                    bye=0
                self.image[row][column] = pygame.transform.scale(self.image[row][column], (Graphics.stnsize, Graphics.stnsize))#サイズ変更
                self.screen.blit(self.image[row][column], (-1000*bye+78*column+39-Graphics.stnsize/2, 78*row+39-Graphics.stnsize/2))#駒を描画
            
        #画面への反映
        pygame.display.update()

 #       #タイマーを今の持ち時間から再セット（再開して一秒後に数字が減るように）
 #       self.timer_set(self.time, self.current_turn)
        
    def timer_set(self, time, current_turn):#time秒のカウントダウンのセット
        self.turnfinish = 0#誰かの手番中状態にする
        self.current_turn = current_turn
        self.time = time+1#持ち時間のスタート秒数（update実行時に１減るので調整）
 #       pygame.time.set_timer(self.countdown, 1000)#1000ミリ秒ごとにself.countdownが発生？する
        #数字の画像作成
        text_time = self.font.render(str(self.time), True, (255, 255, 255))
        text_time = pygame.transform.scale(text_time, (60, 60))#サイズ調整

        text_zero = self.font.render("0", True, (255, 255, 255))#表示する時間の画像作成
        text_zero = pygame.transform.scale(text_zero, (60, 60))#サイズ調整

        #現在（次）の手番を示す＠マークの表示
        if self.current_turn == 1:#黒の手番のとき
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_white[0]+35,self.timer_white[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(text_zero, (self.timer_white[0]+35,self.timer_white[1]+85))#0の描画
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_white[0]+130-30,self.timer_white[1]+25, 20,20))#白の＠を消す
            self.screen.blit(pygame.transform.scale(self.font.render("@", True, (100, 100, 255)), (20,20)), (self.timer_black[0]+130-30,self.timer_black[1]+25))
        else:#白の手番のとき
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_black[0]+35,self.timer_black[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(text_zero, (self.timer_black[0]+35,self.timer_black[1]+85))#0の描画
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_black[0]+130-30,self.timer_black[1]+25, 20,20))#黒の＠を消す
            self.screen.blit(pygame.transform.scale(self.font.render("@", True, (255, 255, 255)), (20,20)), (self.timer_white[0]+130-30,self.timer_white[1]+25))
        
        self.timer_update()
    
        
    def timer_update(self):#タイマーの数字更新 turn1:黒-1:白
        #タイムアップの処理（turnfinishを１にする）
        if self.time == 0:#表示されている数字が0になっていたら終了
#            self.countdown = 0#カウントダウンのイベントを消去
            self.turnfinish = 1#手番終了　Gra.timer(turnfinish=0)→タイマー終了（turnfinish=1)
            return#この命令をぬける
        #カウントダウン（今から表示する数字）
        self.time += -1
        #数字の描画
        text_time = self.font.render(str(self.time), True, (255, 255, 255))#表示する時間の画像作成
        text_time = pygame.transform.scale(text_time, (60, 60))#サイズ調整
        if self.current_turn == 1:#黒の手番のとき
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_black[0]+35,self.timer_black[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(text_time, (self.timer_black[0]+35,self.timer_black[1]+85))#数字の描画
        else:#白の手番のとき
            pygame.draw.rect(self.screen, (0,0,0), (self.timer_white[0]+35,self.timer_white[1]+85,60,60))#前の数字を黒で塗りつぶす
            self.screen.blit(text_time, (self.timer_white[0]+35,self.timer_white[1]+85))#数字の描画

        #画面への反映
        pygame.display.update()
    
    def pop_with_button_on_board(self, fulltext, l, r, color):
        if color == "green":
            color_r, color_g, color_b = (0, 150, 0)
        elif color == "blue":
            color_r, color_g, color_b = (0, 0, 150)
        elif color == "red":
            color_r, color_g, color_b = (150, 0, 0)
        else:
            print("color?")
            return
        pygame.draw.rect(self.screen, (color_r, color_g, color_b), (self.pop_on_board_bg))
        
        ev_od = 0
        if len(fulltext) % 2 == 1:
            ev_od = 1
        for i in range(len(fulltext)):
            self.text_l[i] = self.font.render(fulltext[i], True, (255,255,255))
            if self.text_l[i].get_rect().width > self.pop_on_board_bg.width:
                self.text_l[i] = pygame.transform.scale(self.text_l[i], (self.pop_on_board_bg.width, self.text_l[i].get_rect().height))
            self.text_l_rect[i] = self.text_l[i].get_rect()
            self.text_l_rect[i].center = (self.pop_on_board_bg.centerx, (self.pop_on_board_bg.top+ self.pop_on_board_leftbutton.top)/2 + (self.text_l_rect[i].height)*(i+1 - ((len(fulltext)-ev_od)/2+1))+(self.text_l_rect[i].height/2)*(1-ev_od))
            self.screen.blit(self.text_l[i], self.text_l_rect[i])
        
        self.button[0] = l
        self.button[1] = r
        for i in {0,1}:
            self.text_b[i] = self.font.render(self.button[i], True, (255,255,255))
            if self.text_b[i].get_rect().width > self.pop_on_board_bg.width:
                self.text_b[i] = pygame.transform.scale(self.text_b[i], (self.pop_on_board_bg.width, self.text_b[i].get_rect().height))
            self.text_b_rect[i] = self.text_b[i].get_rect()
            if i == 0:
                self.text_b_rect[0].center = self.pop_on_board_leftbutton.center
            if i == 1:
                self.text_b_rect[1].center = self.pop_on_board_rightbutton.center

        
        pygame.draw.rect(self.screen, (color_r+30, color_g+30, color_b+30), self.pop_on_board_leftbutton)
        pygame.draw.rect(self.screen, (color_r+30, color_g+30, color_b+30), self.pop_on_board_rightbutton)
        self.screen.blit(self.text_b[0], self.text_b_rect[0])
        self.screen.blit(self.text_b[1], self.text_b_rect[1])

        pygame.display.update()
    
    def pop_on_board(self, fulltext, color):
        pygame.draw.rect(self.screen, color, (self.pop_on_board_bg))

        ev_od = 0
        if len(fulltext) % 2 == 1:
            ev_od = 1
        for i in range(len(fulltext)):
            self.text_l[i] = self.font.render(fulltext[i], True, (255,255,255))
            if self.text_l[i].get_rect().width > self.pop_on_board_bg.width:
                self.text_l[i] = pygame.transform.scale(self.text_l[i], (self.pop_on_board_bg.width, self.text_l[i].get_rect().height))
            self.text_l_rect[i] = self.text_l[i].get_rect()
            self.text_l_rect[i].center = (self.pop_on_board_bg.centerx, self.pop_on_board_bg.centery + (self.text_l_rect[i].height)*(i+1 - ((len(fulltext)-ev_od)/2+1)))
            self.screen.blit(self.text_l[i], self.text_l_rect[i])

        #画面への反映
        pygame.display.update()

        pygame.time.set_timer(Graphics.pop_pass_delete, 1000)#5000ミリ秒ごとにself.pop_deleteが発生？する


        
    def pop_conclusion(self, position, black_number, white_number):
        #リザルト数値の用意
        text_result_number = "Black"+str(black_number)+" - "+str(white_number)+"white"
        #勝利者別メッセージ用意
        if position == 1:#黒の勝ちメッセージ用意
            text_winner = "Black is winner"
        elif position == 0:
            text_winner = "Draw..."
        else:#白の勝ちメッセージ用意
            text_winner = "White is winner"
        
        self.pop_with_button_on_board([text_winner, text_result_number], "restart", "end", "blue")

        #画面への反映
        pygame.display.update()

    def pop_surrender(self):#本当に降参するのか確認popの表示
        self.pop_with_button_on_board([Graphics.text_pop_surrender], "yes", "no", "red")
    
    def pop_pause(self):#pausepopの表示
        self.pop_with_button_on_board(["pause"], "restart", "return", "green")
    
    def pop_invalid(self, i):#置けない場所を選んだ時のポップ
        if i == 0:
            self.draw_on_window(Graphics.text_pop_invalid, (78*8+(1000-78*8)/2, 78*4 - 39, 1000-78*8, 50), (255,255,255))
        if i == 1:
            self.draw_on_window(0, (78*8+(1000-78*8)/2, 78*4 - 39, 1000-78*8, 50), (0,0,0))

    
    def pop_pass(self):#ぱすのポップ
        #ポップ描画
        pygame.draw.rect(self.screen, (0,100,100), self.pop_surrender_bg)
        
        self.screen.blit(self.text_pop_pass_image, (self.text_pop_pass_rect))#テキストを指定の座標に表示
        #画面への反映
        pygame.display.update()

        pygame.time.set_timer(Graphics.pop_pass_delete, 1000)#5000ミリ秒ごとにself.pop_deleteが発生？する

    def pop_delete(self):#pop消去
        pygame.time.set_timer(Graphics.pop_pass_delete, 0)
        #緑色の盤面を再描画
        pygame.draw.rect(self.screen, (100,255,100), (0,0,78*8,78*8))
        #盤面のgridを描画
        for i in range(7):
            pygame.draw.line(self.screen, (100,100,200), (78*(i+1),0), (78*(i+1),78*8),3)
        for i in range(7):
            pygame.draw.line(self.screen, (100,100,200), (0,78*(i+1)), (78*8,78*(i+1)),3)
        self.board_update(self.state)

    def draw_on_window(self, moji, rect, color):
        if moji == 0:
            rect = pygame.Rect(rect)
            rect.center = rect.left, rect.top
            pygame.draw.rect(self.screen, color, pygame.Rect(rect))
            return
        self.text = self.font.render(moji, True, color)
        if rect[2] > 0 and rect[3] >0:
            self.text = pygame.transform.scale(self.text, (rect[2], rect[3]))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (rect[0], rect[1])
      #  pygame.draw.rect(self.screen, (0,0,0), self.text_rect)
        self.screen.blit(self.text, self.text_rect)

    def ai_think(self,i):
        if i == 0:
            self.draw_on_window(0, (78*4, 78*4, 156, 55),(0,150,0))
            self.draw_on_window("..........", (78*4, 78*4, 156, 55),(255,255,255))
        if i == 1:
            #緑色の盤面を描画
            pygame.draw.rect(self.screen, (100,255,100), (0,0,78*8,78*8))
            #盤面のgridを描画
            for i in range(7):
                pygame.draw.line(self.screen, (100,100,200), (78*(i+1),0), (78*(i+1),78*8),3)
            for i in range(7):
                pygame.draw.line(self.screen, (100,100,200), (0,78*(i+1)), (78*8,78*(i+1)),3)
            self.board_update(self.state)  # 盤面はboard.gridに合わせる
    
    
