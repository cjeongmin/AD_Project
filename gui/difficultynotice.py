import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__package__))+"/chess")
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QHBoxLayout, QDialog, QToolButton


class Button(QToolButton):
    def __init__(self, text, x, y, callback, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setStyleSheet("font-size: 28px;")
        self.setFixedSize(200, 100)
        self.setGeometry(x, y, 100, 100)
        self.clicked.connect(callback)

class DifficultyNotice(QDialog):
    EASY = 10
    NORMAL = 100
    HARD = 1000

    def __init__(self, ai):
        super().__init__()
        self.ai = ai
        self.initUI()


    def initUI(self):
        self.easy = Button("Easy", 75, 25, self.buttonClicked, self)
        self.normal = Button("Normal",75, 150, self.buttonClicked ,self)
        self.hard = Button("Hard", 75, 275, self.buttonClicked, self)

        self.setFixedSize(350, 400)
        self.setGeometry(0, 0, 350, 400)
        self.setWindowTitle("Options")
        self.setCenter()
        self.show()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttonClicked(self):
        text = self.sender().text()
        if text == "Easy":
            self.ai.searcher.depth = DifficultyNotice.EASY
            self.ai.time = 0.001
        elif text == "Normal":
            self.ai.searcher.depth = DifficultyNotice.NORMAL
            self.ai.time = 0.2
        elif text == "Hard":
            self.ai.searcher.depth = DifficultyNotice.HARD
            self.ai.time = 0.5
        self.deleteLater()

    def closeEvent(self, event):
        event.ignore()