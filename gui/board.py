import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__package__))+"/chess")

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QToolButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QMouseEvent
import copy

from .tile import Tile
from .promotionnotice import PromotionNotice
from .endnotice import EndNotice
from ai.ai import AI
from gui.difficultynotice import DifficultyNotice
import copy

from chess.team import Team
from chess.position import Position
from chess.check import fillCheckBoard, checkmate, staleMate
from chess.pieces.pawn import Pawn
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.rook import Rook
from chess.pieces.queen import Queen
from chess.pieces.king import King

"""
TODO:
1. 프로모션 완성 # 해결
2. 캐슬링 # 해결
3. 앙파상 # 해결
4. 자신이 핀에 걸린 상태인지 확인 # 해결
5. 체크일때 왕 움직이기 # 해결
6. 체크메이트 #해결
7. 특정 말이 움직일 때, 킹이 체크가 걸리는 쪽은 못 움직이도록 하기 #해결
8. 스테일메이트 #해결
"""

class Board(QWidget):
    def __init__(self, chessBoard, ai=None):
        super().__init__()
        self.oriChessBoard = copy.deepcopy(chessBoard)
        self.chessBoard = chessBoard
        self.ai = ai
        self.tiles = []
        self.lastMove = []
        self.pickedPiece = None
        self.edge = None
        self.checkEdge = None
        self.notice = None
        self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
        self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
        # self.repaintBoard()
        self.initUI()
        self.setCenter()

    def initUI(self):
        self.setFixedSize(800, 800)
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle("Chess")
        self.selectMode()

        self.show()


    def selectMode(self):
        self.mainPalette = QPalette()
        self.mainPalette.setBrush(10, QBrush(QImage(os.path.dirname(os.path.abspath(__file__))+'/images/chessboard.png').scaled(QSize(800, 800))))
        self.setPalette(self.mainPalette)
        
        self.singleButton = QToolButton(self)
        self.singleButton.setText("Single Mode")
        self.setStyleSheet("font-size: 28px;")
        self.singleButton.setGeometry(150, 200, 500, 100)
        self.singleButton.clicked.connect(self.callback)

        self.aiButton = QToolButton(self)
        self.aiButton.setText("AI Mode")
        self.setStyleSheet("font-size: 28px;")
        self.aiButton.setGeometry(150, 500, 500, 100)
        self.aiButton.clicked.connect(self.callback)


    def callback(self):
        self.mode = self.sender().text()
        
        if self.mode == "Single Mode":
            self.ai = None
        elif self.mode == "AI Mode":
            self.ai = AI()
            notice = DifficultyNotice(self.ai)
            notice.exec_()
            print(self.ai.searcher.depth)

        self.singleButton.hide()
        self.aiButton.hide()

        self.turn = Team.WHITE
        self.drawBoard()


    def drawBoard(self):
        # 체스 보드를 배경화면으로 설정
        self.chessPalette = QPalette()
        self.chessPalette.setBrush(10, QBrush(QImage(os.path.dirname(os.path.abspath(__file__))+'/images/chessboard.png').scaled(QSize(800, 800))))
        self.setPalette(self.chessPalette)
        
        self.repaintBoard()

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
                self.lastMove = [self.pickedPiece.pos, piece.pos]
                if self.pickedPiece.getType() == "Pawn":
                    #미리 움직여서 왕이 체크인지 확인. 체크이면 리턴
                    preBoard = copy.deepcopy(self.chessBoard)
                    prePiece = copy.deepcopy(self.pickedPiece)
                    preSuccess = prePiece.move(Position(piece.pos['x'], piece.pos['y']), preBoard)[0]

                    if not(preSuccess):
                        return
                    check = fillCheckBoard(preBoard, prePiece.team)[1]
                    if check:
                        return 

                    #실제 움직임
                    success, promotion = self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard)
                    if not(success):
                        return
                    else:
                        if promotion:
                            self.notice = PromotionNotice(self.pickedPiece.team, self.chessBoard, Position(self.pickedPiece.pos['x'], self.pickedPiece.pos['y']))
                            self.notice.exec_()
                elif self.pickedPiece.getType() != "King":
                    #미리 움직임
                    preBoard = copy.deepcopy(self.chessBoard)
                    prePiece = copy.deepcopy(self.pickedPiece)
                    preSuccess = prePiece.move(Position(piece.pos['x'], piece.pos['y']), preBoard)

                    if not(preSuccess):
                        return
                    check = fillCheckBoard(preBoard, prePiece.team)[1]
                    if check:
                        return
                        
                    #실제 움직임
                    if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard)):
                        return
                else: # King
                    if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard)):
                        return
                # try:
                self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
                self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
                # except:
                #     notice = EndNotice(self.turn)
                #     notice.exec_()
                #     self.deleteLater()
                self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
                self.edge.hide()
                self.edge.deleteLater()
                self.edge = None
                self.repaintBoard()
                self.repaint()
                if self.ai != None and len(self.lastMove) == 2:
                    self.aiMove()
                    self.repaintBoard()
                self.pickedPiece = None
            else:
                return

    def mousePressEvent(self, e):
        x, y = e.x()//100, e.y()//100
        if self.pickedPiece != None:
            self.lastMove = [self.pickedPiece.pos, Position(x, y)]
            if self.pickedPiece.getType() == "Pawn":
                #미리 움직여서 왕이 체크인지 확인. 체크이면 리턴
                preBoard = copy.deepcopy(self.chessBoard)
                prePiece = copy.deepcopy(self.pickedPiece)
                preSuccess = prePiece.move(Position(x, y), preBoard)[0]
                if not(preSuccess):
                    return
                check = fillCheckBoard(preBoard, prePiece.team)[1]
                if check:
                    return 

                #실제 움직임
                success, promotion = self.pickedPiece.move(Position(x, y), self.chessBoard)
                if not(success):
                    return
                else:
                    if promotion:
                        self.notice = PromotionNotice(self.pickedPiece.team, self.chessBoard, Position(x, y))
                        self.notice.exec_()
            elif self.pickedPiece.getType() != "King":
                #미리 움직여서 왕이 체크인지 확인. 체크이면 리턴
                preBoard = copy.deepcopy(self.chessBoard)
                prePiece = copy.deepcopy(self.pickedPiece)
                preSuccess = prePiece.move(Position(x, y), preBoard)
                if not(preSuccess):
                    return
                check = fillCheckBoard(preBoard, prePiece.team)[1]
                if check:
                    return 

                #실제 움직임
                if not(self.pickedPiece.move(Position(x, y), self.chessBoard)):
                    return
            else:
                if not(self.pickedPiece.move(Position(x, y), self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard)):
                    return
            self.pickedPiece = None
            self.edge.hide()
            self.edge.deleteLater()
            self.edge = None
            # try:
            self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
            self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
            # except:
                # notice = EndNotice(self.turn)
                # notice.exec_()
                # self.deleteLater()
            self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
            self.repaintBoard()
            self.repaint()
            if self.ai != None and len(self.lastMove) == 2:
                self.aiMove()
                self.repaintBoard()

    def repaintBoard(self):
        ck = None
        for tile in self.tiles:
            tile.deleteLater()
        self.tiles = []
        if self.checkEdge != None:
            self.checkEdge.hide()
            self.checkEdge.deleteLater()
            self.checkEdge = None

        for y in range(8):
            for x in range(8):
                if self.chessBoard[y][x] == None:
                    continue
                # 폰의 dieByEnpassant 값을 내림.
                if self.chessBoard[y][x].getType() == "Pawn":
                    if self.chessBoard[y][x].dieByEnpassant > 0:
                        self.chessBoard[y][x].dieByEnpassant -= 1
                # 킹이 체크인 경우 하이라이팅
                elif self.chessBoard[y][x].getType() == "King":
                    if self.chessBoard[y][x].team == self.turn and (self.whiteCheck if self.turn == Team.WHITE else self.blackCheck):
                        self.checkEdge = QLabel(self)
                        self.checkEdge.setPixmap(QPixmap(os.path.dirname(os.path.abspath(__file__))+'/images/rededge.png'))
                        self.checkEdge.move(x*100, y*100)
                        self.checkEdge.show()

                        #체크메이트 확인
                        ck = checkmate(self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard, self.turn)
                        if ck:
                            print("CheckMate", ck)
                        else:
                            print("Check", ck)

                tile = Tile(self.chessBoard[y][x], self)
                self.tiles.append(tile)
                tile.setGeometry(x*100, y*100, 100, 100)
                tile.clicked.connect(self.pickPiece)
                tile.show()

        self.setWindowTitle(f"Chess: {Team.BLACK if self.turn == Team.BLACK else Team.WHITE}")
        if ck:
            notice = EndNotice(Team.BLACK if self.turn == Team.WHITE else Team.WHITE)
            notice.exec_()
            self.singleButton.show()
            self.aiButton.show()
            self.chessBoard = copy.deepcopy(self.oriChessBoard)
            self.setPalette(self.mainPalette)
            for tile in self.tiles:
                tile.deleteLater()
            self.tiles = []
            self.lastMove = []
            if self.edge != None:
                self.edge.deleteLater()
                self.edge = None
            self.pickedPiece = None
            if self.checkEdge != None:
                self.checkEdge.deleteLater()
                self.checkEdge = None
            if self.notice != None:
                self.notice.deleteLater()
                self.notice = None
            self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
            self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
            self.repaint()


        #스테일메이트 확인
        stm = staleMate(self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard, self.turn)
        if stm:
            print("StaleMate", self.turn)

        #스테일메이트 확인
        stm = staleMate(self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard, self.turn)
        if stm:
            print("StaleMate", self.turn)

    # def reduceValueOfPawnEnpassant(self):
    #     for y in range(8):
    #         for x in range(8):
    #             if self.chessBoard[y][x] != None and self.chessBoard[y][x].getType() == "Pawn":
    #                 if self.chessBoard[y][x].dieByEnpassant > 0:
    #                     self.chessBoard[y][x].dieByEnpassant -= 1

    def aiMove(self):
        self.setWindowTitle("Chess: AI")

        # parse
        move = ""
        for p in self.lastMove:
            move += chr(p['x']+ord('a'))+str(8-p['y'])
        print(f"player move: {move}")
        self.ai.hist.append(self.ai.hist[-1].move((self.ai.parse(move[:2]), self.ai.parse(move[2:]))))
        self.ai.print_pos(self.ai.hist[-1].rotate())

        # search
        start = time.time()
        for _, move, _ in self.ai.searcher.search(self.ai.hist[-1], self.ai.hist):
            if time.time() - start > self.ai.time:
                break

        # move
        self.ai.hist.append(self.ai.hist[-1].move(move))
        move = self.ai.render(119-move[0])+self.ai.render(119-move[1])
        print(f"ai move: {move}")
        x1, y1, x2, y2 = ord(move[0])-ord('a'), 8-int(move[1]), ord(move[2])-ord('a'), 8-int(move[3])

        self.ai.print_pos(self.ai.hist[-1])

        if self.chessBoard[y1][x1].getType() == "Pawn":
            piece = self.chessBoard[y1][x1]
            _, promotion = piece.move(Position(x2, y2), self.chessBoard)
            if promotion:
                self.chessBoard[y2][x2] = Queen(piece.pos, piece.team)
        elif self.chessBoard[y1][x1].getType() == "King":
            self.chessBoard[y1][x1].move(Position(x2, y2), self.chessBoard, self.blackCheckBoard)
        else:
            self.chessBoard[y1][x1].move(Position(x2, y2), self.chessBoard)
        # refresh CheckBoard
        self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
        self.blackCheckBoard, self.BlackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
        self.turn = Team.WHITE

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    


# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = Board()
    # sys.exit(app.exec_())