from Move import Move

class GameState:
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves,
                              'N': self.get_knight_moves, 'B': self.get_bishop_moves,
                              'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.enPassantPossible = ()
        self.pins = []
        self.checks = []
        self.inCheck = False

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        print(f"Moved {move.pieceMoved} from ({move.startRow}, {move.startCol}) to ({move.endRow}, {move.endCol})")
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # en passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        # set enPassantPossible
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    def undo_move(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enPassantPossible = move.enPassantPossiblePrevious

    def get_valid_moves(self):
        moves = self.get_all_moves()
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.in_check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo_move()
        return moves

    def in_check(self):
        self.find_pins_and_checks()
        return self.inCheck

    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    # Pawn moves with promotion and en passant
    def get_pawn_moves(self, r, c, moves):
        direction = -1 if self.whiteToMove else 1
        startRow = 6 if self.whiteToMove else 1
        enemyColor = 'b' if self.whiteToMove else 'w'
        # 1-square move
        if self.board[r+direction][c] == "--":
            promotion = (r + direction == 0 or r + direction == 7)
            moves.append(Move((r,c), (r+direction,c), self.board, isPawnPromotion=promotion))
            if r == startRow and self.board[r+2*direction][c] == "--":
                moves.append(Move((r,c), (r+2*direction,c), self.board, isPawnTwo=True))
        # captures
        for dc in (-1,1):
            c2 = c + dc
            if 0 <= c2 < 8:
                if self.board[r+direction][c2][0] == enemyColor:
                    promotion = (r + direction == 0 or r + direction == 7)
                    moves.append(Move((r,c), (r+direction,c2), self.board, pieceCaptured=self.board[r+direction][c2], isPawnPromotion=promotion))
                elif (r+direction, c2) == self.enPassantPossible:
                    moves.append(Move((r,c),(r+direction,c2),self.board,isEnpassantMove=True,pieceCaptured=enemyColor+'P'))

    # Rook, Knight, Bishop, Queen, King similar to tutorial code
    def get_rook_moves(self, r, c, moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemy = 'b' if self.whiteToMove else 'w'
        for dr,dc in directions:
            for i in range(1,8):
                r2, c2 = r+dr*i, c+dc*i
                if not (0 <= r2 <8 and 0<=c2<8): break
                target = self.board[r2][c2]
                if target == "--":
                    moves.append(Move((r,c),(r2,c2),self.board))
                elif target[0] == enemy:
                    moves.append(Move((r,c),(r2,c2),self.board,pieceCaptured=target))
                    break
                else:
                    break

    def get_bishop_moves(self, r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemy = 'b' if self.whiteToMove else 'w'
        for dr,dc in directions:
            for i in range(1,8):
                r2,c2 = r+dr*i, c+dc*i
                if not (0<=r2<8 and 0<=c2<8): break
                target = self.board[r2][c2]
                if target == "--":
                    moves.append(Move((r,c),(r2,c2),self.board))
                elif target[0] == enemy:
                    moves.append(Move((r,c),(r2,c2),self.board,pieceCaptured=target))
                    break
                else:
                    break

    def get_knight_moves(self, r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        ally = 'w' if self.whiteToMove else 'b'
        for dr,dc in knightMoves:
            r2,c2 = r+dr,c+dc
            if 0<=r2<8 and 0<=c2<8:
                target = self.board[r2][c2]
                if target[0] != ally:
                    moves.append(Move((r,c),(r2,c2),self.board,pieceCaptured=target if target!='--' else "--"))

    def get_queen_moves(self, r,c,moves):
        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r,c,moves)

    def get_king_moves(self, r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        ally = 'w' if self.whiteToMove else 'b'
        for dr,dc in directions:
            r2,c2 = r+dr,c+dc
            if 0<=r2<8 and 0<=c2<8:
                target = self.board[r2][c2]
                if target[0] != ally:
                    moves.append(Move((r,c),(r2,c2),self.board,pieceCaptured=target if target!='--' else "--"))

    def find_pins_and_checks(self):
        self.inCheck = False 
