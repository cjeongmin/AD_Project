from PyQt5.QtWidgets import QApplication, QDesktopWidget, QHBoxLayout, QDialog, QLabel

class EndNotice(QDialog):
    def __init__(self, team):
        super().__init__()
        self.initUI(team)

    def initUI(self, team):
        self.setFixedSize(150, 50)
        self.setGeometry(0, 0, 150, 50)
        self.setWindowTitle("End")
        hbox = QHBoxLayout()
        label = QLabel(f"{team} Win")
        hbox.addWidget(label)
        self.setLayout(hbox)
        self.setCenter()
        self.show()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())