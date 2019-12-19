import unittest

from chessBoard import *
from chess.check import fillCheckBoard, checkmate, staleMate
from chess.team import Team

from chess.pieces.pawn import Pawn
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.rook import Rook
from chess.pieces.queen import Queen
from chess.pieces.king import King


class TestChess(unittest.TestCase):
    def setUp(self):

        self.init = chessBoard_init
        self.ck_init = checkBoard_init
        
        self.checkMate = chessBoard_checkMate
        self.ck_checkMate = checkBoard_checkMate
        
        self.check = chessBoard_check
        self.ck_check = checkBoard_check
    
        self.staleMate = chessBoard_staleMate
        self.ck_staleMate = checkBoard_staleMate

        self.pawn = pawn_board
        self.rook = rook_board
        self.bishop = bishop_board
        self.knight = knight_board
        self.queen = queen_board

        self.promotion = chessBoard_promotion
        
    def tearDown(self):
        pass

    
    def test_checkmate(self):
        self.assertTrue(checkmate(self.checkMate, self.ck_checkMate,Team.WHITE))
        self.assertFalse(checkmate(self.init, self.ck_init,Team.WHITE))
        self.assertFalse(checkmate(self.staleMate, self.ck_staleMate, Team.WHITE))
        self.assertFalse(checkmate(self.check, self.ck_check, Team.WHITE))

    def test_stalekmate(self):
        self.assertFalse(staleMate(self.checkMate, self.ck_checkMate,Team.WHITE))
        self.assertFalse(staleMate(self.init, self.ck_init,Team.WHITE))
        self.assertTrue(staleMate(self.staleMate, self.ck_staleMate, Team.WHITE))
        self.assertFalse(staleMate(self.check, self.ck_check, Team.WHITE))

    def test_check(self):
        self.assertTrue(fillCheckBoard(self.checkMate,Team.WHITE)[1])
        self.assertFalse(fillCheckBoard(self.init, Team.WHITE)[1])
        self.assertFalse(fillCheckBoard(self.staleMate, Team.WHITE)[1])
        self.assertTrue(fillCheckBoard(self.check, Team.WHITE)[1])

    def test_move(self):
        self.assertFalse(self.pawn[4][4].move(Position(3, 4), self.pawn)[0])
        self.assertTrue(self.pawn[4][4].move(Position(4, 2), self.pawn)[0])

        self.assertFalse(self.rook[4][4].move(Position(3, 3), self.rook))
        self.assertTrue(self.rook[4][4].move(Position(0, 4), self.rook))

        self.assertFalse(self.knight[4][4].move(Position(4, 2), self.knight))
        self.assertTrue(self.knight[4][4].move(Position(3, 2), self.knight))

        self.assertFalse(self.bishop[4][4].move(Position(0, 4), self.bishop))
        self.assertTrue(self.bishop[4][4].move(Position(3, 3), self.bishop))

        self.assertFalse(self.queen[4][4].move(Position(3, 20), self.queen))
        self.assertTrue(self.queen[4][4].move(Position(2, 2), self.queen))

    def test_promotion(self):
        self.assertFalse(self.promotion[2][7].move(Position(7, 1), self.promotion)[1])
        self.assertTrue(self.promotion[1][7].move(Position(7, 0), self.promotion)[1])


if __name__ == "__main__":
    unittest.main()