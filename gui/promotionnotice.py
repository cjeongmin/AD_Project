import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__package__))+"/chess")
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QHBoxLayout, QDialog

from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.rook import Rook
from chess.pieces.queen import Queen
from chess.position import Position
from chess.team import Team
from chess.position import Position
from .tile import Tile

class PromotionNotice(QDialog):
    def __init__(self, team: Team, chessboard, pos: Position):
        super().__init__()
        self.chessboard = chessboard
        self.pos = pos
        self.pieces = [Tile(Queen(pos, team)), Tile(Rook(pos, team)), Tile(Bishop(pos, team)),Tile(Knight(pos, team))]
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 150)
        self.setGeometry(0, 0, 600, 150)
        self.setWindowTitle("Promotion")
        self.setCenter()
        hbox = QHBoxLayout()
        for piece in self.pieces:
            hbox.addWidget(piece)
            piece.clicked.connect(self.pickPiece)
        self.setLayout(hbox)
        self.show()

        
    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def pickPiece(self):
        self.piece = self.sender().piece
        self.chessboard[self.pos['y']][self.pos['x']] = self.piece
        self.deleteLater()

    def closeEvent(self, event):
        event.ignore()

# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = PromotionNotice(Team.WHITE)
    # sys.exit(app.exec_())