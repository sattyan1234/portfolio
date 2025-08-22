#「盤面サイズ、初期配置、駒を置ける場所の定義」、「現在の手番が置ける場所の更新、確認」、「駒を置く,ひっくり返す,盤面の更新」、「ゲームの終了判定(全マス埋まる)」、「駒の数」

class Board:
    #オセロ盤の初期化
    def __init__(self):
        #オセロ版の初期状態
        self.size = 8  #8x8の盤面、一辺のマスの数を指定する。
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]  #0は空白,1は黒,2は白 
        ##初期配置（中央に4つの石を配置）
        self.grid[3][3] = self.grid[4][4] = 2  #白石
        self.grid[3][4] = self.grid[4][3] = 1  #黒石

        #駒を置けない場合に自動的にパスできるように、おける場所を事前に計算しておく
        self.valid_move = {1: set(), 2: set()}  # 黒:1, 白:2 の置ける場所を辞書で管理する
        self.update_valid(1)
        self.update_valid(2)

    #各色の駒を置ける場所を更新する
    def update_valid(self, current_turn):
        #現在の手番の置ける場所をリセット
        self.valid_move[current_turn] = set()
        #現在の手番の置ける場所を確認、更新
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] == 0 and self.accept_moving(x, y, current_turn):
                    self.valid_move[current_turn].add((x,y))
    
        #現在の手番がおける駒の場所を返す
    def get_valid(self, current_turn):
        return self.valid_move[current_turn]


    #駒を置けるかの判定
    #入力は置こうとしている駒の座標(横:x,縦:y)と置こうとしている人の手番
    #置けるならば"True"、置けなければ"False"を返す
    def accept_moving(self, x, y, current_turn):
        #おこうとしている場所に駒がある場合
        if self.grid[y][x] != 0:
            return False
        
        #周囲8方向のチェック準備
        tyekku = [(-1,-1),(0,-1),(-1,0),(1,-1),(1,0),(-1,1),(0,1),(1,1)]#8方向
        #相手の色の確認
        if current_turn == 1:
            color = 2
        else:
            color = 1

        #8方向を確認する
        for dx, dy in tyekku:
            nx, ny = x + dx, y + dy#8方向の座標を設定
            found_opponent = False
            #空白か自分の駒が出るまでに相手の駒がどれだけ続くか確認
            while 0 <= nx < self.size and 0 <= ny < self.size:
                #相手の駒であればok
                if self.grid[ny][nx] == color:
                    found_opponent = True
                #自分の駒があり、相手の駒を挟んでいれば有効手
                elif self.grid[ny][nx] == current_turn:
                    if found_opponent:
                        return True
                    break
                #空白ならば別の場所を探す
                else:
                    break
                #より1マス奥の座標に更新
                nx += dx
                ny += dy
        #全ての方向が無効であれば、置けない
        return False
    

    #駒を置き、ひっくり返す
    #入力は置こうとしている駒の座標(横:x,縦:y)と置こうとしている人の手番
    #駒を置き、ひっくり返し、盤面を更新する
    def reversi(self, x, y, current_turn):
        #指定の場所に駒を置く
        self.grid[y][x] = current_turn

        #周囲8方向のチェック準備
        tyekku = [(-1,-1),(0,-1),(-1,0),(1,-1),(1,0),(-1,1),(0,1),(1,1)]#8方向
        #相手の色の確認
        color = 2 - (current_turn // 2 )

        #8方向を確認し、反転可能な駒をひっくり返す
        for dx, dy in tyekku:
            nx, ny = x + dx, y + dy#8方向の座標を設定
            reversilist = []#1方向ごとに相手の駒の座標をメモしておく

            #空白か自分の駒が出るまでに相手の駒がどれだけ続くか確認
            while 0 <= nx < self.size and 0 <= ny < self.size:
                if self.grid[ny][nx] == color:#隣が相手の駒なら
                    reversilist.append((nx, ny))
                elif self.grid[ny][nx] == current_turn:#隣が自分の駒なら
                    #ひっくり返す駒があるなら、間の相手の駒を自分の駒に更新
                    if reversilist:
                        for fx, fy in reversilist:
                            self.grid[fy][fx] = current_turn
                            #print(dx, dy,fx,fy,reversilist,self.grid[fy][fx])
                    break
                else:
                    break
                #より1マス奥の座標に更新
                nx += dx
                ny += dy

    #全マス埋まっているかの確認
    #終わっていれば"True"、終わっていなければ"Flase"を返す
    def full_gameover(self):
        for row in self.grid:
            if 0 in row:
                return False
        return True
    
    #黒の数と白の数を数える
    def count_piece(self):
        black_count = sum(row.count(1) for row in self.grid)
        white_count = sum(row.count(2) for row in self.grid)
        #それぞれの駒の数を返す
        return black_count, white_count

#パスを利用したゲーム終了判定はクラスを統合したosero.pyで実装したい。