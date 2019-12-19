import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__package__))+"/chess")

from chess.pieces.pawn import Pawn
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.rook import Rook
from chess.pieces.queen import Queen
from chess.pieces.king import King

from chess.position import Position
from chess.team import Team
from chess.check import *

chessBoard_init = [
        [
            Rook(Position(0, 0), Team.BLACK), Knight(Position(1, 0), Team.BLACK), Bishop(Position(2, 0), Team.BLACK), Queen(Position(3, 0), Team.BLACK), King(Position(4, 0), Team.BLACK), Bishop(Position(5, 0), Team.BLACK), Knight(Position(6, 0), Team.BLACK), Rook(Position(7, 0), Team.BLACK)
        ],
        [
            Pawn(Position(x, 1), Team.BLACK) for x in range(8)
        ],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [
            Pawn(Position(x, 6), Team.WHITE) for x in range(8)
        ],
        [
            Rook(Position(0, 7), Team.WHITE), Knight(Position(1, 7), Team.WHITE), Bishop(Position(2, 7), Team.WHITE), Queen(Position(3, 7), Team.WHITE), King(Position(4, 7), Team.WHITE), Bishop(Position(5, 7), Team.WHITE), Knight(Position(6, 7), Team.WHITE), Rook(Position(7, 7), Team.WHITE)
        ],
        
    ]
checkBoard_init = fillCheckBoard(chessBoard_init, Team.WHITE)[0]

chessBoard_checkMate = [
        [
            Rook(Position(0, 0), Team.BLACK), Knight(Position(1, 0), Team.BLACK), Bishop(Position(2, 0), Team.BLACK), None, King(Position(4, 0), Team.BLACK), Bishop(Position(5, 0), Team.BLACK), Knight(Position(6, 0), Team.BLACK), Rook(Position(7, 0), Team.BLACK)
        ],
        [
            Pawn(Position(x, 1), Team.BLACK) if x != 4 else None for x in range(8)
        ],
        [None if x != 4 else Pawn(Position(x, 2), Team.BLACK) for x in range(8)],
        [None for _ in range(8)],
        [None if x != 6 else Pawn(Position(x, 4), Team.WHITE) for x in range(7)] + [Queen(Position(7, 4), Team.BLACK)],
        [None if x != 5 else Pawn(Position(x, 5), Team.WHITE) for x in range(8)],
        [
            Pawn(Position(x, 6), Team.WHITE) if x != 5 and x != 6 else None for x in range(8)
        ],
        [
            Rook(Position(0, 7), Team.WHITE), Knight(Position(1, 7), Team.WHITE), Bishop(Position(2, 7), Team.WHITE), Queen(Position(3, 7), Team.WHITE), King(Position(4, 7), Team.WHITE), Bishop(Position(5, 7), Team.WHITE), Knight(Position(6, 7), Team.WHITE), Rook(Position(7, 7), Team.WHITE)
        ],
    ]
checkBoard_checkMate = fillCheckBoard(chessBoard_checkMate, Team.WHITE)[0]

chessBoard_staleMate = [
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None if x != 0 else King(Position(x, 5), Team.BLACK) for x in range(8)],
        [None for _ in range(8)],
        [King(Position(0, 7), Team.WHITE), Bishop(Position(1, 7), Team.WHITE)] + [None for _ in range(5)] + [Rook(Position(7, 7), Team.BLACK)],
    ]
checkBoard_staleMate = fillCheckBoard(chessBoard_staleMate, Team.WHITE)[0]

chessBoard_check = [
        [
            Rook(Position(0, 0), Team.BLACK), Knight(Position(1, 0), Team.BLACK), Bishop(Position(2, 0), Team.BLACK), None, King(Position(4, 0), Team.BLACK), Bishop(Position(5, 0), Team.BLACK), Knight(Position(6, 0), Team.BLACK), Rook(Position(7, 0), Team.BLACK)
        ],
        [
            Pawn(Position(x, 1), Team.BLACK) if x != 3 else None for x in range(8)
        ],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(3)] + [Pawn(Position(4, 4), Team.WHITE), Queen(Position(5, 4), Team.BLACK)] + [None for _ in range(3)],
        [None for _ in range(8)],
        [
            Pawn(Position(x, 6), Team.WHITE) if x != 3 and x != 4 else None for x in range(8)
        ],
        [
            Rook(Position(0, 7), Team.WHITE), Knight(Position(1, 7), Team.WHITE), Bishop(Position(2, 7), Team.WHITE), Queen(Position(3, 7), Team.WHITE), King(Position(4, 7), Team.WHITE), Bishop(Position(5, 7), Team.WHITE), Knight(Position(6, 7), Team.WHITE), Rook(Position(7, 7), Team.WHITE)
        ],
    ]
checkBoard_check = fillCheckBoard(chessBoard_check, Team.WHITE)[0]