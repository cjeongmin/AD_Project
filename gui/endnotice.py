from PyQt5.QtWidgets import QApplication, QDesktopWidget, QHBoxLayout, QDialog, QLabel

class EndNotice(QDialog):
    def __init__(self, team, state):
        super().__init__()
        self.initUI(team, state)

    def initUI(self, team, state):
        self.setFixedSize(150, 50)
        self.setGeometry(0, 0, 150, 50)
        self.setWindowTitle("End")
        hbox = QHBoxLayout()
        if state == "Checkmate":
            label = QLabel(f"{team} Win")
        elif state == "Stalemate":
            label = QLabel("StaleMate")
        hbox.addWidget(label)
        self.setLayout(hbox)
        self.setCenter()
        self.show()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())