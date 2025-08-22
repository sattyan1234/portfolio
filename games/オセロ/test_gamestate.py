import unittest
from gamestate import GameState
from board import Board  # 駒の数を数えるために Board クラスを使用

class TestGameState(unittest.TestCase):

    def setUp(self):
        """ 各テスト前に `GameState` を初期化 """
        self.state = GameState()
        self.board = Board()

    def test_switch_turn(self):
        """ 手番の交代が正しく行われるかテスト """
        first_turn = self.state.current_turn
        self.state.swich_turn()
        self.assertIn(self.state.current_turn, [1, 2])  # 手番は 1 または 2 のはず
        self.assertNotEqual(self.state.current_turn, first_turn)  # 手番が変わっていることを確認

    def test_pass_reset(self):
        """ パスカウントのリセットをテスト """
        self.state.pass_UP()
        self.state.pass_reset()
        self.assertEqual(self.state.pass_count, 0)

    def test_pass_up(self):
        """ パスカウントの増加をテスト """
        self.state.pass_UP()
        self.assertEqual(self.state.pass_count, 1)
        self.state.pass_UP()
        self.assertEqual(self.state.pass_count, 2)

    def test_count_winner(self):
        """ 盤面の駒の数で勝者が正しく決まるかテスト """
        # 初期状態では黒と白が 2 個ずつなので引き分けのはず
        self.state.count_winner(self.board)
        self.assertEqual(self.state.winner, 0)

        # 黒を増やして勝者を黒にする
        self.board.grid[0][0] = 1  # 黒を1つ増やす
        self.state.count_winner(self.board)
        self.assertEqual(self.state.winner, 1)  # 黒が勝つ

        # 白を増やして勝者を白にする
        self.board.grid[0][1] = 2  # 白を1つ増やす
        self.board.grid[0][2] = 2  # 白を1つ増やす
        self.state.count_winner(self.board)
        self.assertEqual(self.state.winner, 2)  # 白が勝つ

    def test_surrender(self):
        """ 降参した場合、相手が勝者になるかテスト """
        self.state.current_turn = 1  # 黒のターン
        self.state.surrender()
        self.assertEqual(self.state.winner, 2)  # 白が勝者

        self.state.current_turn = 2  # 白のターン
        self.state.surrender()
        self.assertEqual(self.state.winner, 1)  # 黒が勝者

if __name__ == '__main__':
    unittest.main()