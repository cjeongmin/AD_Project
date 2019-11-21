import sys, os
sys.path.insert(0, "/home/cjm/AD_Project/chess")

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QMouseEvent

from .tile import Tile
from chess.team import Team
from chess.position import Position

class Board(QWidget):
    def __init__(self, chessBoard):
        super().__init__()
        self.chessBoard = chessBoard
        self.tiles = []
        self.turn = Team.WHITE
        self.pickedPiece = None
        self.edge = None
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
                if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard)):
                    return
                self.repaintBoard()
                self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
                self.pickedPiece = None
                self.edge.deleteLater()
                self.edge = None
            else:
                return

    def mousePressEvent(self, e):
        x, y = e.x()//100, e.y()//100
        if self.pickedPiece != None:
            if not(self.pickedPiece.move(Position(x, y), self.chessBoard)):
                return
            self.repaintBoard()
            self.pickedPiece = None
            self.edge.deleteLater()
            self.edge = None
            self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE

    def repaintBoard(self):
        for tile in self.tiles:
            tile.deleteLater()
        self.tiles = []
        for y in range(8):
            for x in range(8):
                if self.chessBoard[y][x] == None:
                    continue
                tile = Tile(self.chessBoard[y][x], self)
                self.tiles.append(tile)
                tile.setGeometry(x*100, y*100, 100, 100)
                tile.clicked.connect(self.pickPiece)
                tile.show()
        self.setWindowTitle(f"Chess: {Team.BLACK if self.turn != Team.BLACK else Team.WHITE}")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    


# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = Board()
    # sys.exit(app.exec_())