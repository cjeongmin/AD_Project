from chess.team import Team
import copy
from chess.position import Position

class End(Exception):
    pass

def fillCheckBoard(chessBoard, team: Team):#왕이 갈 수 있는 곳, 왕이 체크인지 확인
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

def checkmate(chessBoard, checkBoard, team: Team):  #True : 체크메이트, False : 체크 / 해당 메서드는 체크 일 경우 호출
    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
    checkNum = 0
    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] == None:
                continue
            if team == chessBoard[y][x].team and chessBoard[y][x].getType() == "King":
                if checkBoard[y][x] == True:
                    return False
                for i in range(8):
                    nx, ny = x + dx[i], y + dy[i]
                    #King이 움직일 수 있으면 Not CheckMate

                    if (0 <= ny < 8 and 0 <= nx < 8):
                        if checkBoard[ny][nx] == True:
                            print("King can move")
                            return False
            if team != chessBoard[y][x].team and chessBoard[y][x].kingCheck == True:
                checkNum += 1
    #Check를 건 말이 2개 이상이면 CheckMate
    if checkNum > 1:
        print("Check Piece is over 2")
        return True
    return canMove(chessBoard, checkBoard, team)

#왕 이외에 모든 말이 움직여서 체크가 아닌 경우의 수가 있으면 False, 모든 경우의 수가 체크이면 True
def canMove(chessBoard, checkBoard, team: Team):
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
                            success = piece.move(Position(x1, y1), board)[0]
                            if success:
                                Check = fillCheckBoard(board, piece.team)[1]
                                if not(Check):
                                    return False
                        if 0 <= x2 < 8:
                            board = copy.deepcopy(chessBoard)
                            piece = board[y][x]
                            success = piece.move(Position(x2, y1), board)[0]
                            if success:
                                Check = fillCheckBoard(board, piece.team)[1]
                                if not(Check):
                                    return False
                    if 0 <= y2 < 8:
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        success = piece.move(Position(x, y2), board)[0]
                        if success:
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False
                    if 0 <= y3 < 8 and chessBoard[y][x].isFirstMove is True:
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        success = piece.move(Position(x, y3), board)[0]
                        if success:
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False
                elif chessBoard[y][x].getType() == "Bishop":
                    dx, dy = [1, 1, -1 ,-1], [-1, 1, 1, -1]
                    for i in range(4):
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (board[y1][x1] is None or (board[y1][x1].getType() == "King" and board[y1][x1].team != piece.team)):
                            success = piece.move(Position(x1, y1), board)
                            Check = fillCheckBoard(board, board[y1][x1].team)[1]
                            if not(Check):
                                return False
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            success = piece.move(Position(x1, y1), board)
                            Check = fillCheckBoard(board, piece.team)[1]
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
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False
                            
                elif chessBoard[y][x].getType() == "Rook":
                    dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
                    for i in range(4):
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (board[y1][x1] is None or (board[y1][x1].getType() == "King" and board[y1][x1].team != piece.team)):
                            success = piece.move(Position(x1, y1), board)
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            success = piece.move(Position(x1, y1), board)
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False
                elif chessBoard[y][x].getType() == "Queen":
                    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
                    for i in range(4):
                        board = copy.deepcopy(chessBoard)
                        piece = board[y][x]
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (board[y1][x1] is None or (board[y1][x1].getType() == "King" and board[y1][x1].team != piece.team)):
                            success = piece.move(Position(x1, y1), board)
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False
                            y1 += dy[i]
                            x1 += dx[i]
                        if (0 <= x1 < 8 and 0 <= y1 < 8):
                            success = piece.move(Position(x1, y1), board)
                            Check = fillCheckBoard(board, piece.team)[1]
                            if not(Check):
                                return False            
    return True

def staleMate(chessBoard, checkBoard, team: Team):  #True : 스테일메이트, False : 계속 진행 / 해당 메서드는 매 회 호출
    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] == None:
                continue
            if chessBoard[y][x].team == team and chessBoard[y][x].getType() == "King":
                if checkBoard[y][x] == False:
                    return False
                for i in range(8):
                    nx, ny = x + dx[i], y + dy[i]
                    if (0 <= ny < 8 and 0 <= nx < 8):
                        if checkBoard[ny][nx] == True:
                            return False
                break
    
    return canMove(chessBoard, checkBoard, team)