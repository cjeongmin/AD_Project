import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__package__))+"/chess")

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QMouseEvent
import copy

from .tile import Tile
from .promotionnotice import PromotionNotice
from .endnotice import EndNotice

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
        self.chessBoard = chessBoard
        self.ai = ai
        self.tiles = []
        self.turn = Team.WHITE
        self.lastMove = []
        self.pickedPiece = None
        self.edge = None
        self.checkEdge = None
        self.notice = None
        self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
        self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
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
                            # self.repaintBoard()
                elif self.pickedPiece.getType() != "King":
                    preBoard = copy.deepcopy(self.chessBoard)
                    prePiece = copy.deepcopy(self.pickedPiece)
                    preSuccess = prePiece.move(Position(piece.pos['x'], piece.pos['y']), preBoard)

                    if not(preSuccess):
                        return
                    check = fillCheckBoard(preBoard, prePiece.team)[1]
                    if check:
                        return 
                    
                    if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard)):
                        return
                else: # King
                    if not(self.pickedPiece.move(Position(piece.pos['x'], piece.pos['y']), self.chessBoard, self.whiteCheckBoard if self.turn == Team.WHITE else self.blackCheckBoard)):
                        return
                try:
                    self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
                    self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
                except:
                    notice = EndNotice(self.turn)
                    notice.exec_()
                    self.deleteLater()
                self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
                self.repaintBoard()
                self.pickedPiece = None
                self.edge.deleteLater()
                self.edge = None
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
                        self.repaintBoard()
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
            self.edge.deleteLater()
            self.edge = None
            try:
                self.blackCheckBoard, self.blackCheck = fillCheckBoard(self.chessBoard, Team.BLACK)
                self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)
            except:
                notice = EndNotice(self.turn)
                notice.exec_()
                self.deleteLater()
            self.turn = Team.BLACK if self.turn == Team.WHITE else Team.WHITE
            self.repaintBoard()

    def repaintBoard(self):
        for tile in self.tiles:
            tile.deleteLater()
        self.tiles = []
        if self.checkEdge != None:
            self.checkEdge.deleteLater()
            self.checkEdge = None
        
        # AI MOVE
        if self.ai != None and self.turn == Team.BLACK:
            def print_board(board):
                print()
                uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                            'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
                for i, row in enumerate(board.board.split()):
                    print(' ', 8-i, ' '.join(uni_pieces.get(p, p) for p in row))
                print('    a b c d e f g h \n\n')
            
            self.setWindowTitle(f"Chess: AI")
            self.turn = Team.WHITE

            # parse
            move = ""
            for p in self.lastMove:
                move += chr(p['x']+ord('a'))+str(8-p['y'])
            self.ai.hist.append(self.ai.hist[-1].move((self.ai.parse(move[:2]), self.ai.parse(move[2:]))))

            # search
            start = time.time()
            for _, move, _ in self.ai.searcher.search(self.ai.hist[-1], self.ai.hist):
                if time.time() - start > 0.00001:
                    break

            # move
            self.ai.hist.append(self.ai.hist[-1].move(move))
            move = self.ai.render(119-move[0])+self.ai.render(119-move[1])
            x1, y1, x2, y2 = ord(move[0])-ord('a'), 8-int(move[1]), ord(move[2])-ord('a'), 8-int(move[3])

            if self.chessBoard[y1][x1].getType() == "King":
                self.chessBoard[y1][x1].move(Position(x2, y2), self.chessBoard, self.blackCheckBoard)
            else:
                self.chessBoard[y1][x1].move(Position(x2, y2), self.chessBoard)
            # refresh whiteCheckBoard
            self.whiteCheckBoard, self.whiteCheck = fillCheckBoard(self.chessBoard, Team.WHITE)

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

        # self.reduceValueOfPawnEnpassant()

        for line in self.chessBoard:
            for piece in line:
                print(piece, end="")
            print()
        print("*" * 20)
        self.setWindowTitle(f"Chess: {Team.BLACK if self.turn == Team.BLACK else Team.WHITE}")

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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    


# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # ex = Board()
    # sys.exit(app.exec_())