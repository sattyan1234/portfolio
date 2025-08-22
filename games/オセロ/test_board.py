import unittest
from board import Board  # `Board` クラスをインポート

class TestBoard(unittest.TestCase):

    def setUp(self):
        """ 各テスト前に `Board` を初期化 """
        self.board = Board()

    def test_initial_setup(self):
        """ 盤面の初期化が正しく行われているかテスト """
        self.assertEqual(self.board.size, 8)  # 盤面サイズが 8x8 であることを確認

        # 初期配置が正しいか確認
        expected_grid = [[0] * 8 for _ in range(8)]
        expected_grid[3][3] = expected_grid[4][4] = 2  # 白石
        expected_grid[3][4] = expected_grid[4][3] = 1  # 黒石
        self.assertEqual(self.board.grid, expected_grid)

    def test_getvalid(self):
        """ 現在の手番で駒を置ける場所が正しく取得できるかテスト """
        black_valid_moves = self.board.getvalid(1)
        white_valid_moves = self.board.getvalid(2)

        # 初期状態で黒が置ける場所
        expected_black_moves = {(2, 3), (3, 2), (4, 5), (5, 4)}
        expected_white_moves = {(2, 4), (3, 5), (4, 2), (5, 3)}

        self.assertEqual(black_valid_moves, expected_black_moves)
        self.assertEqual(white_valid_moves, expected_white_moves)

    def test_acceptmoving(self):
        """ 駒を置けるかの判定が正しいかテスト """
        self.assertTrue(self.board.acceptmoving(2, 3, 1))  # 黒が(2,3)に置けるか
        self.assertFalse(self.board.acceptmoving(3, 3, 1))  # すでに白石(2)がある場所
        self.assertFalse(self.board.acceptmoving(0, 0, 1))  # 何も挟めない場所

    def test_reversi(self):
        """ 駒を置いたときに正しくひっくり返るかテスト """
        if self.board.acceptmoving(2, 3, 1):
            self.board.reversi(2, 3, 1)  # 黒を(2,3)に置く
            self.assertEqual(self.board.grid[3][3], 1)  # ひっくり返して(3,3)が黒になる
        if self.board.acceptmoving(2, 4, 2):
            self.board.reversi(2, 4, 2)  # 白を(2,4)に置く
            #print(self.board.grid)
            self.assertEqual(self.board.grid[4][3], 2)  # ひっくり返して(3,4)が白になる

    def test_updatevalid(self):
        self.setUp()
        """ 駒を置ける場所の更新が正しく行われるかテスト """
        self.board.reversi(2, 3, 1)  # 黒を(2,3)に置く
        self.board.updatevalid(2)  # 白の置ける場所を更新

        expected_white_moves_after = {(2, 2), (4, 2), (2, 4)}
        self.assertEqual(self.board.getvalid(2), expected_white_moves_after)

    def test_fullgameover(self):
        """ 全マス埋まったときにゲーム終了判定が正しく行われるかテスト """
        self.assertFalse(self.board.fullgameover())  # 初期状態では False

        # 盤面をすべて埋める
        self.board.grid = [[1] * 8 for _ in range(8)]
        self.assertTrue(self.board.fullgameover())  # すべて埋まれば True

    def test_countpiece(self):
        """ 駒の数が正しくカウントできるかテスト """
        black, white = self.board.countpiece()
        self.assertEqual(black, 2)  # 初期状態では黒が 2 個
        self.assertEqual(white, 2)  # 初期状態では白が 2 個

        # 黒の駒を増やす
        self.board.grid[0][0] = 1
        self.board.grid[1][1] = 1
        black, white = self.board.countpiece()
        self.assertEqual(black, 4)  # 黒が 4 個

        # 白の駒を増やす
        self.board.grid[0][1] = 2
        self.board.grid[1][0] = 2
        black, white = self.board.countpiece()
        self.assertEqual(white, 4)  # 白が 4 個

if __name__ == '__main__':
    unittest.main()