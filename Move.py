class Move:
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, pieceCaptured="--",
                 isPawnPromotion=False, isEnpassantMove=False, isPawnTwo=False):
        self.startRow, self.startCol = startSq
        self.endRow, self.endCol = endSq
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = pieceCaptured
        self.isPawnPromotion = isPawnPromotion
        self.isEnpassantMove = isEnpassantMove
        self.isPawnTwo = isPawnTwo
        self.enPassantPossiblePrevious = board

    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.startRow == other.startRow and self.startCol == other.startCol
                and self.endRow == other.endRow and self.endCol == other.endCol and
                self.pieceMoved == other.pieceMoved and self.pieceCaptured == other.pieceCaptured)
