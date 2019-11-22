from chess.team import Team

# 수정 필요함
def fillCheckBoard(chessBoard, team: Team):
    kingPos = []
    src = [[True for _ in range(8)] for _ in range(8)]
    for y in range(8):
        for x in range(8):
            if chessBoard[y][x] == None:
                continue
            if team == chessBoard[y][x].team and chessBoard[y][x].getType() == "King":
                kingPos = [x, y]
                continue

            if team == chessBoard[y][x].team:
                src[y][x] = False
            else:
                piece = chessBoard[y][x]
                if piece.getType() == "Pawn":
                    x1, x2, y1 = x-1, x+1, y + (-1 if piece.team == Team.WHITE else 1)
                    if 0 <= y1 < 8:
                        if 0 <= x1 < 8:
                            src[y1][x1] = False
                        if 0 <= x2 < 8:
                            src[y1][x2] = False
                elif piece.getType() == "Bishop":
                    dx, dy = [1, 1, -1 ,-1], [-1, 1, 1, -1]
                    for i in range(4):
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            src[y1][x1] = False
                            y1 += dy[i]
                            x1 += dx[i]
                elif piece.getType() == "Knight":
                    dx, dy = [-2, -1, 1, 2, 2, 1, -1, -2], [1, 2, 2, 1, -1, -2, -2, -1]
                    for i in range(8):
                        nx, ny = x+dx[i], y+dy[i]
                        if (0 <= ny < 8 and 0 <= nx < 8):
                            src[ny][nx] = False
                elif piece.getType() == "Rook":
                    dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
                    for i in range(4):
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            src[y1][x1] = False
                            y1 += dy[i]
                            x1 += dx[i]
                elif piece.getType() == "Queen":
                    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
                    for i in range(8):
                        x1, y1 = x + dx[i], y + dy[i]
                        while (0 <= x1 < 8 and 0 <= y1 < 8) and (chessBoard[y1][x1] is None or (chessBoard[y1][x1].getType() == "King" and chessBoard[y1][x1].team != piece.team)):
                            src[y1][x1] = False
                            y1 += dy[i]
                            x1 += dx[i]
                elif piece.getType() == "King":
                    dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
                    for i in range(8):
                        nx, ny = x+dx[i], y+dy[i]
                        if (0 <= ny < 8 and 0 <= nx < 8):
                            src[ny][nx] = False
                            
    return (src, True) if not(src[kingPos[1]][kingPos[0]]) else (src, False) # 공격받으면 True 아니면 False