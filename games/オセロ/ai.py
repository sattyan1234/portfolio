# ai.py
import random
import time

class AI:
    def __init__(self, difficulty='normal'):
        # AIの難易度設定（'easy', 'normal', 'hard'）
        self.difficulty = difficulty
        # 盤面の各位置の評価値（角や端は高い評価値）
        self.position_weights = [
            [100, -10, 8, 6, 6, 8, -10, 100],
            [-10, -25, -4, -4, -4, -4, -25, -10],
            [8, -4, 6, 4, 4, 6, -4, 8],
            [6, -4, 4, 0, 0, 4, -4, 6],
            [6, -4, 4, 0, 0, 4, -4, 6],
            [8, -4, 6, 4, 4, 6, -4, 8],
            [-10, -25, -4, -4, -4, -4, -25, -10],
            [100, -10, 8, 6, 6, 8, -10, 100]
        ]
    
    def get_move(self, board, player):
        """AIの手を決定する関数"""
        valid_moves = board.get_valid(player)
        
        # 有効な手がない場合はNoneを返す
        if not valid_moves:
            return None
        
        # 難易度に応じた選択方法
        if self.difficulty == 'easy':
            # 簡単：ランダムに選択
            return random.choice(list(valid_moves))
        
        elif self.difficulty == 'normal':
            # 標準：位置の評価値を考慮
            return self._evaluate_position(board, valid_moves, player)
        
        elif self.difficulty == 'hard':
            # 難しい：ミニマックスアルゴリズムで数手先を読む
            return self._minimax_move(board, valid_moves, player)
    
    def _evaluate_position(self, board, valid_moves, player):
        """位置の評価値に基づいて手を選択"""
        best_score = -float('inf')
        best_move = None
        
        for move in valid_moves:
            y, x = move
            # 位置の評価値
            score = self.position_weights[y][x]
            
            # よりランダム性を持たせるために少しの乱数を加える（同点の場合の選択に影響）
            score += random.uniform(0, 5)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        # 少し「考えている」感を出すための遅延
        self.thinking_time = random.uniform(0.5, 2)
        return best_move
    
    def _minimax_move(self, board, valid_moves, player):
        """ミニマックスアルゴリズムを使用して最適な手を選択（難しいレベル用）"""
        best_score = -float('inf')
        best_move = None
        
        # ボードの一時的なコピーを作成する関数
        def copy_board(original_board):
            return [row[:] for row in original_board.grid]
        
        # 評価関数（盤面の状態を数値化）
        def evaluate_board(board_state, player):
            opponent = 3 - player  # 相手のプレイヤー番号（1→2, 2→1）
            player_count = sum(row.count(player) for row in board_state)
            opponent_count = sum(row.count(opponent) for row in board_state)
            
            # 盤面の位置による評価
            position_score = 0
            for y in range(8):
                for x in range(8):
                    if board_state[y][x] == player:
                        position_score += self.position_weights[y][x]
                    elif board_state[y][x] == opponent:
                        position_score -= self.position_weights[y][x]
            
            # 終盤では石の数を重視
            if player_count + opponent_count > 50:
                return position_score + 2 * (player_count - opponent_count)
            else:
                return position_score
        
        # 簡易版のリバースシミュレーション（AIの内部計算用）
        def simulate_reversi(board_state, y, x, player):
            new_board = [row[:] for row in board_state]
            new_board[y][x] = player
            
            # 8方向のベクトル
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            opponent = 3 - player
            
            for dy, dx in directions:
                # その方向にある相手の石を確認
                pieces_to_flip = []
                ny, nx = y + dy, x + dx
                
                while 0 <= ny < 8 and 0 <= nx < 8 and new_board[ny][nx] == opponent:
                    pieces_to_flip.append((ny, nx))
                    ny += dy
                    nx += dx
                
                # その方向の先に自分の石があれば挟める
                if 0 <= ny < 8 and 0 <= nx < 8 and new_board[ny][nx] == player and pieces_to_flip:
                    for flip_y, flip_x in pieces_to_flip:
                        new_board[flip_y][flip_x] = player
            
            return new_board
        
        # ミニマックスアルゴリズム（深さ2まで）
        for move in valid_moves:
            y, x = move
            # この手を打った後の盤面をシミュレーション
            new_board_state = simulate_reversi(copy_board(board), y, x, player)
            
            # 相手の最善手を予測
            opponent = 3 - player
            opponent_best_score = float('inf')
            
            # 相手の有効な手をシミュレーション
            opponent_has_move = False
            
            # シンプルな有効手チェック（実際のゲームロジックとは異なる簡易版）
            for oy in range(8):
                for ox in range(8):
                    if new_board_state[oy][ox] != 0:
                        continue
                    
                    # この位置が有効かどうかを簡易チェック
                    valid = False
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    
                    for dy, dx in directions:
                        ny, nx = oy + dy, ox + dx
                        if not (0 <= ny < 8 and 0 <= nx < 8 and new_board_state[ny][nx] == player):
                            continue
                        
                        valid = True
                        break
                    
                    if valid:
                        opponent_has_move = True
                        opponent_new_board = simulate_reversi(new_board_state, oy, ox, opponent)
                        opponent_score = evaluate_board(opponent_new_board, player)
                        opponent_best_score = min(opponent_best_score, opponent_score)
            
            # 相手が手を打てない場合は自分の盤面評価をそのまま使用
            if not opponent_has_move:
                score = evaluate_board(new_board_state, player)
            else:
                score = opponent_best_score
            
            if score > best_score:
                best_score = score
                best_move = move
        
        # 最適な手が見つからなかった場合はランダムに選択
        if best_move is None:
            best_move = random.choice(list(valid_moves))
        
        # 「考えている」感を出すための遅延
        self.thinking_time = random.uniform(1.0, 5)
        return best_move