import sys, os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush

class Board(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(800, 800)
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle("Chess")

        # 체스 보드를 배경화면으로 설정
        self.chessboard = QImage(os.path.dirname(os.path.abspath(__file__))+'/images/chessboard.png').scaled(QSize(800, 800))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.chessboard))
        self.setPalette(palette)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Board()
    sys.exit(app.exec_())