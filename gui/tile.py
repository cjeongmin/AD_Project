import sys, os

from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter, QPixmap

from chess.team import Team

class Tile(QAbstractButton):
    __PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, piece=None, parent=None):
        super(Tile, self).__init__(parent)
        self.piece = piece
        self.image = self.selectImage()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.image = self.selectImage()
        painter.drawPixmap(event.rect(), self.image)

    def selectImage(self):
        if self.piece == None:
            return
        pieceType = self.piece.getType()
        if pieceType == "King":
            if self.piece.team == Team.WHITE:
                return QPixmap(self.__PATH+"/images/whiteking.png")
            else:
                return QPixmap(self.__PATH+"/images/blackking.png")
        elif pieceType == "Queen":
            if self.piece.team == Team.WHITE:
                return QPixmap(self.__PATH+"/images/whitequeen.png")
            else:
                return QPixmap(self.__PATH+"/images/blackqueen.png")
        elif pieceType == "Knight":
            if self.piece.team == Team.WHITE:
                return QPixmap(self.__PATH+"/images/whiteknight.png")
            else:
                return QPixmap(self.__PATH+"/images/blackknight.png")
        elif pieceType == "Rook":
            if self.piece.team == Team.WHITE:
                return QPixmap(self.__PATH+"/images/whiterook.png")
            else:
                return QPixmap(self.__PATH+"/images/blackrook.png")
        elif pieceType == "Bishop":
            if self.piece.team == Team.WHITE:
                return QPixmap(self.__PATH+"/images/whitebishop.png")
            else:
                return QPixmap(self.__PATH+"/images/blackbishop.png")
        elif pieceType == "Pawn":
            if self.piece.team == Team.WHITE:
                return QPixmap(self.__PATH+"/images/whitepawn.png")
            else:
                return QPixmap(self.__PATH+"/images/blackpawn.png")

    def sizeHint(self):
        if self.image == None:
            return
        return self.image.size()

    def __str__(self):
        return f"{self.piece}"