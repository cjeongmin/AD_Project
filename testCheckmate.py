import unittest

from chessBoard import *
from chess.check import fillCheckBoard, checkmate, staleMate
from chess.team import Team


class TestCheckMate(unittest.TestCase):
    def setUp(self):
        self.init = chessBoard_init
        self.ck_init = checkBoard_init
        
        self.checkMate = chessBoard_checkMate
        self.ck_checkMate = checkBoard_checkMate
        
        self.check = chessBoard_check
        self.ck_check = checkBoard_check
    
        self.staleMate = chessBoard_staleMate
        self.ck_staleMate = checkBoard_staleMate

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

if __name__ == "__main__":
    unittest.main()