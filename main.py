import sys

from time import sleep
from os import system

from chess.check import fillCheckBoard

from chessBoard import *

from gui.board import Board
from PyQt5.QtWidgets import QApplication

from ai.ai import AI

def clear():
    system('clear')

def textTest(chessBoard):
    turn = False
    while True:
        clear()
        whiteCheckBoard, whiteCheck = fillCheckBoard(chessBoard, Team.WHITE) #화이트 킹이 체크인지 아닌지, 왕이 움직일 수 있는 공간 검사
        blackCheckBoard, blackCheck = fillCheckBoard(chessBoard, Team.BLACK) #블랙 킹이 체크인지 아닌지, 옹이 움직일 수 있는 공간 검사
        for line in whiteCheckBoard:
            for e in line:
                print(1 if not(e) else 0, end=" ")
            print()
        print("*"*20)
        print("    0    1    2    3    4    5    6    7")
        for idx, line in enumerate(chessBoard):
            print(idx, end=" ")
            for piece in line:
                print(piece, end=" ")
            print(idx)
        print("    0    1    2    3    4    5    6    7")
        print(("White" if not(turn) else "Black") + "'s turn")
        print(f"Check: {blackCheck if turn else whiteCheck}")

        curY, curX = list(map(int, input().split()))
        if curX == -1 and curY == -1:
            break

        pick = chessBoard[curY][curX]
        if pick == None or pick.team != (Team.WHITE if not(turn) else Team.BLACK):
            continue
        print(f"pick: {pick}")

        moveY, moveX = list(map(int, input().split()))

        if pick.getType() != "King":
            if not(pick.move(Position(moveX, moveY), chessBoard)):
                continue
        else:
            if not(pick.move(Position(moveX, moveY), chessBoard, whiteCheckBoard if not(turn) else blackCheckBoard)):
                # 킹이 움직일 때 실패한 경우 사용자에게 경고를 하는 코드가 필요함.
                continue
        turn = not(turn)

    print("Exit")

def guiTest(chessBoard):
    app = QApplication(sys.argv)
    board = Board(chessBoard)
    sys.exit(app.exec_())

if __name__ == "__main__":
    guiTest(chessBoard_init)
    #textTest(chessBoard)