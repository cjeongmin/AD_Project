import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QDragEnterEvent, QDropEvent

from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QDrag
from PyQt5.QtCore import Qt, QMimeData

from .tile import Tile

class Board(QWidget):
    def __init__(self, chessBoard):
        super().__init__()
        ###
        self.tiles = []
        for y in range(8):
            self.tiles.append([])
            for x in range(8):
                if chessBoard[y][x] == None:
                    self.tiles[y].append(None)
                    continue
                self.tiles[y].append(Tile(chessBoard[y][x], self))
                self.tiles[y][x].setGeometry(x*100, y*100, 100, 100)
                self.tiles[y][x].clicked.connect(self.getPiece)
                self.tiles[y][x].show()
        ###
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

    def getPiece(self):
        print(self.sender().piece, self.sender().piece.pos)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        print(f"mouseMoveEvent {e.pos()}")
        mime_data = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mime_data)

        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, e):
        print(e.pos())
        e.accept()

    def dropEvent(self, e):
        print(e.pos())

# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = Board()
    # sys.exit(app.exec_())