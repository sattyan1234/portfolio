import pygame
from pygame.locals import *
import sys
import math
import time
import datetime
import random
from board import Board
from gamestate import GameState
from graphics import Graphics
from inputer import Inputer
from ai import AI  

#self.gamestate.current_turn = 1
#board_state = [[0 for _ in range(8)] for _ in range(8)]
class Osero:
    # ゲームスタートの準備
    def __init__(self, player_type=None):
        pygame.init()
        # 各クラスのインスタンスを作成する。このタイミングで各クラスのinit関数が実行される。
        self.board = Board()  # 盤面はboard.gridに合わせる
        self.gamestate = GameState()  # current_turnはここにあわせる
        self.graphics = Graphics()  # ウィンドウ作成
        self.inputer = Inputer()
        # None: 人間対人間, 1: 黒がAI, 2: 白がAI, 3: AI対AI
    #    self.player_type = player_type if player_type is not None else 0 
    #    if self.player_type > 0:
    #        self.ai = AI(difficulty='hard')  # 難易度は適宜変更可能
        self.ai = AI(difficulty='hard')
        self.current_turn = self.gamestate.current_turn  # 今の手番を他のクラスの手番の変数と対応
        self.graphics.current_turn = self.current_turn
        self.board.update_valid(self.current_turn)
        self.running = True  # ゲームが進行しているならばTrue
        self.clock = pygame.time.Clock()
        self.pop_delete_cd = False#invalidpopを消すまでのカウントダウンをする合図
        self.pop_dl_time = 100#invalidpopの表示時間の目安
        self.player_type = 0

    # 統合したクラスで実装する機能の実装
    def display_update(self):  # 画面更新
        self.graphics.window_clear(self.current_turn, self.player_type)
        self.graphics.board_update(self.board.grid)  # 盤面はboard.gridに合わせる

    def is_ai_turn(self):
        """現在のターンがAIかどうかを判断"""
        if self.player_type == 1 and self.current_turn == 1:  # 黒がAI
            return True
        elif self.player_type == 2 and self.current_turn == 2:  # 白がAI
            return True
        elif self.player_type == 3:  # AI対AI
            return True
        return False

    def handle_turn(self):
        """現在のターンを人間かAIに応じて処理"""
        if self.is_ai_turn():
            self.ai_turn()
        else:
            self.input_player()

    def ai_turn(self):

        self.graphics.timer_set(Graphics.fulltime, self.current_turn)

        self.time = 60*Graphics.fulltime
        self.time_disp = 29

        """AIの手番を処理"""
        # AIの思考中表示などがあると良い
    #    self.graphics.window_clear(self.current_turn)
    #    self.graphics.board_update(self.board.grid)
    #    pygame.display.update()



        
        # 有効な手があるか確認
        self.board.update_valid(self.current_turn)
        if self.board.get_valid(self.current_turn) == set():
            self.gamestate.pass_UP()
            time.sleep(1)
            self.state_pass()
            self.judge()
            return
        
        self.gamestate.pass_reset()

        # AIの手を取得
        ai_move = self.ai.get_move(self.board, self.current_turn)

        #思考中表示
        self.graphics.ai_think(0)
        #画面への反映
 #       pygame.display.update()
        #考えてる時間,この間に人間がpauseボタンをおせる
        pygame.event.clear()
        while True:
            self.clock.tick(60)
            if self.time/60 < self.time_disp:
                if self.time_disp == -1:
                    self.state_pass()
                    self.judge()
                else:
                    self.graphics.timer_update()

                    self.time_disp -= 1
            self.time -= 0.97
            if self.time < (30-self.ai.thinking_time)*60:
                break

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button != 1:
                        break
                    self.place = self.inputer.boardclickwhere(event.pos, event.button, 1, self.graphics)[0]
                    if self.place == "pause":#有効な入力あったら入力処理
                        self.input(event.pos, event.button)
                        #思考中表示
                        self.graphics.ai_think(0)
                        pygame.event.clear()
                        break
        #思考中表示削除
        self.graphics.ai_think(1)



        
        if ai_move:
            # AIの手を適用
            put_y, put_x = ai_move
            self.move(put_y, put_x)
        else:
            # 有効な手がない場合（通常ここには来ないはず）
            self.state_pass()
            self.judge()

    def input_player(self):  # プレイヤーの手番中



        self.graphics.timer_set(Graphics.fulltime, self.current_turn)

        self.time = 60*Graphics.fulltime
        self.time_disp = 29

        self.board.update_valid(self.current_turn)
        if self.board.get_valid(self.current_turn) == set():#置ける場所ない時、pop後judge
            self.gamestate.pass_UP()
            time.sleep(1)
            self.state_pass()
            self.judge()

        self.gamestate.pass_reset()#置ける場所あったら一旦パスリセット

        pygame.event.clear()
        while True:
            self.clock.tick(60)
            if self.pop_delete_cd:
                if self.pop_dl_time == 0:
             #      self.graphics.draw_on_window("you can't put there"
                    self.graphics.pop_invalid(1)
                    self.pop_delete_cd = False
                else:
                    self.pop_dl_time -= 1
            
            if self.time/60 < self.time_disp:
                if self.time_disp == -1:
                    self.state_pass()
                    self.judge()
                else:
                    self.graphics.timer_update()
            #        print(datetime.datetime.now())
                    self.time_disp -= 1
            self.time -= 0.97

                

            
            for event in pygame.event.get():#入力待ち
                if event.type == MOUSEBUTTONDOWN:
                    self.place = self.inputer.boardclickwhere(event.pos, event.button, 1, self.graphics)[0]
                    if self.place != None:#有効な入力あったら入力処理
                        self.input(event.pos, event.button)
                        pygame.event.clear()
                        break
                    break

    def input(self, event_pos, event_button):  # 有効入力の処理
        if self.place == "board":# 置けるなら移動処理、無理なら無効pop
            put_x, put_y = self.inputer.boardclickwhere(event_pos, event_button, 1, self.graphics)[1]
            if (put_y, put_x) in self.board.get_valid(self.current_turn):
                self.move(put_y, put_x)
            else:
                self.graphics.pop_invalid(0)
                #画面への反映
                pygame.display.update()
                self.pop_delete_cd = True
                self.pop_dl_time = 100
                return
        #ボタン押下時
        elif self.place == "surrender":  # 降参
            self.state_surrender()
        elif self.place == "pause":
            self.state_pause()

    def move(self, put_y, put_x):  # 移動処理
        self.board.reversi(put_y, put_x, self.current_turn)  # 盤面データ変更、board.gridが更新される
        self.judge()  # 勝敗判定

    def judge(self):  # 勝敗判定
        if self.gamestate.pass_count == 2:  # 両者（置ける場所ない故の）パスなら勝者をコマ数で判定してから決着へ
            self.gamestate.count_winner(self.board)
            self.state_end()
        elif self.board.full_gameover():  # 盤面がすべて埋まったら勝者をコマ数で判定してから決着へ
            self.gamestate.count_winner(self.board)
            self.state_end()
        else:  # どちらでもなければ普通に手番交代
            self.turn_change()

    def turn_change(self):  # 手番交代
        self.gamestate.swich_turn()  # 手番を示す変数を変更、gamestate.current_turnの１と２が入れ替わる
        self.current_turn = self.gamestate.current_turn
        self.graphics.current_turn = self.gamestate.current_turn
        self.display_update()  # 盤面更新
        
        # 手番処理（人間かAIか）
        self.handle_turn()

    def state_pass(self):#パスpop表示中
        self.graphics.pop_on_board(["pass"], (0,100,100))#表示して１秒後に消して元の場所に戻る
        while True:
            for event in pygame.event.get():
                if event.type == self.graphics.pop_pass_delete:
                    self.graphics.pop_delete()#イベント関数（変数）はここで消去される
                    pygame.event.clear()
                    break
            else:
                continue
            break

    def state_surrender(self):#降参pop表示中
        self.graphics.pop_surrender()
        pygame.event.clear()
        r = True
        while r:#yesなら相手を勝者にして決着、noなら元に戻る
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button != 1:
                        break
                    if self.inputer.pop_lr_click(event.pos) == "leftbutton":
                        self.gamestate.surrender()
                        self.state_end()
                        r = False
                        break
                    elif self.inputer.pop_lr_click(event.pos) == "rightbutton":
                        self.display_update()
                        r = False
                        break

        pygame.event.clear()
        
    def state_pause(self):#ポーズ中
        self.graphics.pop_pause()
        pygame.event.clear()
        r = True
        while r:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button != 1:
                        break
                    self.place =  self.inputer.pop_lr_click(event.pos)
                    if self.place == "leftbutton":
                        time.sleep(0.5)
                        self.restart()
                        r = False
                        break
                    if self.place == "rightbutton":
                        self.display_update()
                        r = False
                        break
        
        pygame.event.clear()


    def state_end(self):#決着pop表示中、ここに来るまでに勝者は決めておく
        self.display_update()#盤面更新
        time.sleep(1)
        black, white = self.board.count_piece()
        self.graphics.pop_conclusion(self.gamestate.winner, black, white)
        pygame.event.clear()
        r = True
        while r:#againならboardとgamestateを初期化して、現在の持ち時間を30に戻して画面更新、endならwindow閉じる
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button != 1:
                        break
                    if self.inputer.pop_lr_click(event.pos) == "leftbutton":
                        self.restart()
                        r = False
                        break
                    elif self.inputer.pop_lr_click(event.pos) == "rightbutton":
                        self.close_window()
                        r = False
                        break
        
        pygame.event.clear()
    
    def startmenu(self):#スタートメニュー中
        self.graphics.start()
        r = True
        while r:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button != 1:
                        break
                    if self.graphics.button_rect["with friend"].collidepoint(event.pos):
                        self.player_type = 0
                        self.display_update()
                        r = False
                        break
                    elif self.graphics.button_rect["with ai"].collidepoint(event.pos):
                        self.player_type = random.randint(1,2)
                        self.display_update()
                        r = False
                        break
                    elif self.graphics.button_rect["watch"].collidepoint(event.pos):
                        self.player_type = 3
                        self.display_update()
                        r = False
                        break
                    elif self.graphics.button_rect["end"].collidepoint(event.pos):
                        self.close_window()


    def restart(self):#ゲーム再スタート
        self.board.__init__()
        self.gamestate.__init__()
        self.current_turn = self.gamestate.current_turn
        self.graphics.current_turn = self.current_turn
        self.graphics.time = Graphics.fulltime
        self.startmenu()
        self.handle_turn()
                        

    def close_window(self):#window消す
        self.running = False
        time.sleep(1)
        pygame.quit()#ウィンドウ消す
        sys.exit()
        


    # ゲームループ
    def run(self):
        self.display_update()
        self.board.update_valid(self.current_turn)
        self.startmenu()
        self.display_update()
        self.handle_turn()  # input_player()の代わりにhandle_turn()を呼び出す


# 実際に実行する(ゲームを開始する)
if __name__ == "__main__":
    # 0: 人間対人間, 1: 黒がAI, 2: 白がAI, 3: AI対AI
    game = Osero(player_type=2)  # ここでは白をAIに設定
    game.run()  # 実行するメソッドが必要