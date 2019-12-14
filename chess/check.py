from chess.team import Team
import copy
from chess.position import Position

class End(Exception):
    pass

def fillCheckBoard(chessBoard, team: Team):
    kingPos = ()
    src = [[True for _ in range(8)] for _ in range(8)]
    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] == None:
                continue
            if team == chessBoard[y][x].team and chessBoard[y][x].getType() == "King":
                kingPos = (x, y)
                break
        if len(kingPos) != 0:
            break

    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] == None:
                continue
            if team == chessBoard[y][x].team and chessBoard[y][x].getType() == "King":
                continue

            if team == chessBoard[y][x].team:
                src[y][x] = False
            else:
                chessBoard[y][x].kingCheck = False
                piece = chessBoard[y][x]
                if piece.getType() == "Pawn":
                    x1, x2, y1 = x-1, x+1, y + (-1 if piece.team == Team.WHITE else 1)
                    if 0 <= y1 < 8:
                        if 0 <= x1 < 8:
                            src[y1][x1] = False
                        if 0 <= x2 < 8:
                            src[y1][x2] = False
                        if kingPos[1] == y1 and (kingPos[0] == x1 or kingPos[0] == x2):
                            piece.kingCheck = True
                elif piece.getType() == "Bishop":
                    dx, dy = [1, 1, -1 ,-1], [-1, 1, 1, -1]
                    for i in range(4):
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            src[y1][x1] = False
                            if(y1 == kingPos[1] and x1 == kingPos[0]):
                                piece.kingCheck = True
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            src[y1][x1] = False
                elif piece.getType() == "Knight":
                    dx, dy = [-2, -1, 1, 2, 2, 1, -1, -2], [1, 2, 2, 1, -1, -2, -2, -1]
                    for i in range(8):
                        nx, ny = x+dx[i], y+dy[i]
                        if (0 <= ny < 8 and 0 <= nx < 8):
                            src[ny][nx] = False
                            if(ny == kingPos[1] and nx == kingPos[0]):
                                piece.kingCheck = True
                elif piece.getType() == "Rook":
                    dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
                    for i in range(4):
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            src[y1][x1] = False
                            if(y1 == kingPos[1] and x1 == kingPos[0]):
                                piece.kingCheck = True
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            src[y1][x1] = False
                elif piece.getType() == "Queen":
                    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
                    for i in range(8):
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            src[y1][x1] = False
                            if(y1 == kingPos[1] and x1 == kingPos[0]):
                                piece.kingCheck = True
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            src[y1][x1] = False
                elif piece.getType() == "King":
                    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
                    for i in range(8):
                        nx, ny = x+dx[i], y+dy[i]
                        if (0 <= ny < 8 and 0 <= nx < 8):
                            src[ny][nx] = False

    if len(kingPos) == 0:
        raise End()

    chessBoard[kingPos[1]][kingPos[0]].isCheck = False
    if not(src[kingPos[1]][kingPos[0]]):
        chessBoard[kingPos[1]][kingPos[0]].isCheck = True
    return (src, chessBoard[kingPos[1]][kingPos[0]].isCheck)
    #(src, True) if not(src[kingPos[1]][kingPos[0]]) else (src, False) # 공격받으면 True 아니면 False

# TODO: 체크메이트 기능의 구현이 필요함.
def checkmate(chessBoard, checkBoard, team: Team):  #True : 체크메이트, False : 체크
    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
    checkNum = 0
    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] == None:
                continue
            if team == chessBoard[y][x].team and chessBoard[y][x].getType() == "King":
                kingPos = (x, y)
                for i in range(8):
                    nx, ny = x + dx[i], y + dy[i]
                    #King이 움직일 수 있으면 Not CheckMate

                    if (0 <= ny < 8 and 0 <= nx < 8):
                        if checkBoard[ny][nx] == True:
                            print("King can move")
                            return False            
            if team != chessBoard[y][x].team and chessBoard[y][x].kingCheck == True:
                checkNum += 1
    #CheckMate를 건 말이 2개 이상이면 CheckMate
    if checkNum > 1:
        print("Check Piece is over 2")
        return True
    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] is None:
                continue
            if chessBoard[y][x].team == team:
                if chessBoard[y][x].getType() == "Pawn":
                    board = copy.deepcopy(chessBoard)
                    x1, x2, y1 = x-1, x+1, y + (-1 if board[y][x].team == Team.WHITE else 1)
                    y2, y3 = y + (-1 if board[y][x].team == Team.WHITE else 1), y + (-2 if board[y][x].team == Team.WHITE else 2)
                    if 0 <= y1 < 8:
                        if 0 <= x1 < 8:
                            board = copy.deepcopy(chessBoard)
                            piece = board[y][x]
                            success, promotion = piece.move(Position(x1, y1), board)
                            if success:
                                CheckBoard, Check = fillCheckBoard(board, piece.team)
                                if not(Check):
                                    return False
                        if 0 <= x2 < 8:
                            board = copy.deepcopy(chessBoard)
                            piece = board[y][x]
                            success, promotion = piece.move(Position(x2, y1), board)
                            if success:
                                CheckBoard, Check = fillCheckBoard(board, piece.team)
                                if not(Check):
                                    return False
                    if 0 <= y2 < 8:
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        success, promotion = piece.move(Position(x, y2), board)
                        if success:
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                    if 0 <= y3 < 8 and chessBoard[y][x].isFirstMove is True:
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        success, promotion = piece.move(Position(x, y3), board)
                        if success:
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                elif chessBoard[y][x].getType() == "Bishop":
                    dx, dy = [1, 1, -1 ,-1], [-1, 1, 1, -1]
                    for i in range(4):
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            success = piece.move(Position(x1, y1), board)
                            CheckBoard, Check = fillCheckBoard(board, board[y1][x1].team)
                            if not(Check):
                                return False
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            success = piece.move(Position(x1, y1), board)
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                elif chessBoard[y][x].getType() == "Knight":
                    dx, dy = [-2, -1, 1, 2, 2, 1, -1, -2], [1, 2, 2, 1, -1, -2, -2, -1]
                    for i in range(8):
                        nx, ny = x+dx[i], y+dy[i]
                        if (0 <= ny < 8 and 0 <= nx < 8):
                            board = copy.deepcopy(chessBoard)
                            piece = board[y][x]
                            success = piece.move(Position(nx, ny), board)
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                            
                elif chessBoard[y][x].getType() == "Rook":
                    dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
                    for i in range(4):
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            success = piece.move(Position(x1, y1), board)
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            success = piece.move(Position(x1, y1), board)
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                elif chessBoard[y][x].getType() == "Queen":
                    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
                    for i in range(4):
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            success = piece.move(Position(x1, y1), board)
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            success = piece.move(Position(x1, y1), board)
                            CheckBoard, Check = fillCheckBoard(board, piece.team)
                            if not(Check):
                                return False
            
    return True