#「現在のターン,パスカウント,勝者 の定義」、「手番の交代」、「パスカウントのリセット」、「パスカウントの増加」、「勝敗判定(数える、降参)」
#先手後手をランダムで決めるためにrandomモジュールをインポート
import random
#駒を数える際にboardの関数を使っているのでインポート
from board import Board

class GameState:
    #ゲーム状態の初期化
    def __init__(self):
        self.current_turn = random.choice([1, 2])  #現在のターンをランダムで決定する。1が黒,2が白
        self.pass_count = 0  # 連続パス回数を記録。パスで増える、打てば0に戻る
        self.winner = None #勝者(0:引き分け, 1:黒, 2:白, None:未決定)

    #手番の交代(1と2)
    def swich_turn(self):
        #現在のターンが1なら2に、2なら1にする
        self.current_turn = 2 - (self.current_turn // 2 )

    #パスカウントのリセット
    def pass_reset(self):
        self.pass_count = 0
    
    #パスカウントの増加
    def pass_UP(self):
        self.pass_count += 1


    #勝敗判定
    #数えて勝者を決定する
    def count_winner(self, board):
        #boardの数える関数を利用して勝者を更新
        black, white = board.count_piece()

        if black > white:
            self.winner = 1
        elif black < white:
            self.winner = 2
        else:
            self.winner = 0

    #降参を押した場合、捜査をしていない方の勝利
    def surrender(self):
        #降参を押していない方が勝者になるように更新
        if self.current_turn == 1:
            self.winner = 2
        else:
            self.winner = 1

