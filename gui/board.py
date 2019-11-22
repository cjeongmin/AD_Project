import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__package__))+"/chess")

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QMouseEvent
import time
from .tile import Tile
from .promotionnotice import PromotionNotice
from chess.team import Team
from chess.position import Position
from chess.check import fillCheckBoard

"""
TODO:
1. 프로모션 완성 # 해결
2. 캐슬링 # 해결
3. 자신이 핀에 걸린 상태인지 확인 // 피스들 현재 위치에서 룩, 퀸, 비숍을 확인 후 있으면 처리
4. 체크일때 왕 움직이기 # 해결
5. 체크메이트
6. 양파상
"""

class Board(QWidget):
    def __init__(self, chessBoard):
        super().__init__()
        self.chessBoard = chessBoard
        self.tiles = []
        self.turn = Team.WHITE
        self.pickedPiece = None
        self.edge = None
        self.checkEdge = None
        self.notice = None
        self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
        self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
        self.repaintBoard()
        self.initUI()
        self.setCenter()
        

    def initUI(self):
        self.setFixedSize(800, 800)
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle("Chess")

        # 체스 보드를 배경화면으로 설정
        palette = QPalette()
        palette.setBrush(10, QBrush(QImage(os.path.dirname(os.path.abspath(__file__))+'/images/chessboard.png').scaled(QSize(800, 800))))
        self.setPalette(palette)
        self.show()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def pickPiece(self):
        piece = self.sender().piece
        if piece.team == self.turn:
            self.pickedPiece = piece
            if self.edge != None:
                self.edge.move(piece.pos['x']*100, piece.pos['y']*100)
            else:
                self.edge = QLabel(self)
                self.edge.setPixmap(QPixmap(os.path.dirname(os.path.abspath(__file__))+'/images/yellowedge.png'))
                self.edge.move(piece.pos['x']*100, piece.pos['y']*100)
                self.edge.show()
        else:
            if self.pickedPiece != None:
                if self.pickedPiece.getType() == "Pawn":
                    success, promotion = self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard)
                    if not(success):
                        return
                    else:
                        if promotion:
                            self.notice = PromotionNotice(self.pickedPiece.team, self.chessBoard, Position(self.pickedPiece.pos['x'], self.pickedPiece.pos['y']))
                            self.notice.exec_()
                            self.repaintBoard()
                elif self.pickedPiece.getType() != "King":
                    if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard)):
                        return
                else: # King
                    if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard)):
                        return
                self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
                self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
                self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
                self.repaintBoard()
                self.pickedPiece = None
                self.edge.deleteLater()
                self.edge = None
            else:
                return

    def mousePressEvent(self, e):
        x, y = e.x()//100, e.y()//100
        if self.pickedPiece != None:
            if self.pickedPiece.getType() == "Pawn":
                success, promotion = self.pickedPiece.move(Position(x, y), self.chessBoard)
                if not(success):
                    return
                else:
                    if promotion:
                        self.notice = PromotionNotice(self.pickedPiece.team, self.chessBoard, Position(x, y))
                        self.notice.exec_()
                        self.repaintBoard()
            elif self.pickedPiece.getType() != "King":
                if not(self.pickedPiece.move(Position(x, y), self.chessBoard)):
                    return
            else:
                if not(self.pickedPiece.move(Position(x, y), self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard)):
                    return
            self.pickedPiece = None
            self.edge.deleteLater()
            self.edge = None
            self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
            self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
            self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
            self.repaintBoard()

    def repaintBoard(self):
        for tile in self.tiles:
            tile.deleteLater()
        self.tiles = []
        if self.checkEdge != None:
            self.checkEdge.deleteLater()
            self.checkEdge = None
        for y in range(8):
            for x in range(8):
                if self.chessBoard[y][x] == None:
                    continue
                # 킹이 체크인 경우 하이라이팅
                if self.chessBoard[y][x].getType() == "King":
                    if self.chessBoard[y][x].team == self.turn and (self.whiteCheck if self.turn == Team.WHITE else self.blackCheck):
                        self.checkEdge = QLabel(self)
                        self.checkEdge.setPixmap(QPixmap(os.path.dirname(os.path.abspath(__file__))+'/images/rededge.png'))
                        self.checkEdge.move(x*100, y*100)
                        self.checkEdge.show()

                tile = Tile(self.chessBoard[y][x], self)
                self.tiles.append(tile)
                tile.setGeometry(x*100, y*100, 100, 100)
                tile.clicked.connect(self.pickPiece)
                tile.show()

        
        self.setWindowTitle(f"Chess: {Team.BLACK if self.turn == Team.BLACK else Team.WHITE}")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    


# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = Board()
    # sys.exit(app.exec_())