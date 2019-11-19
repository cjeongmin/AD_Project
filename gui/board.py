import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

class board(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 0, 300, 400)
        self.setStyleSheet("background-image: url(Images_and_HTML/bg.jpg)")
        self.setWindowTitle("Chess")
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = board()
    sys.exit(app.exec_())