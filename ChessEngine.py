class GameState():
    def __init__(self):
        #-board is 8x8 2d list
        #-first character represents color of piece, b or w
        #-the second character represents type of piece
        #  R=Rook,N=Knight,B=Bishop,Q=Queen,K=King,P=Pawn
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
        self.whiteToMove=True
        self.moveLog= []
    
    '''
    Takes a move as a parameter and executes it
    will not work for castling,pawn promotion, and en-passant
    '''
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) > 0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = [Move((6,4),(4,4),self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'R':
                        self.getRookMoves(r,c,moves)

        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(r,c,moves):
        pass

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getRookMoves(r,c,moves):
        pass

class Move():
    # maps keys to values
    # keys : value
    ranksToRows = {'1':7,'2':6,'3':5,'4':4,
                   '5':3,'6':2,'7':1,'8':0}
    rowToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols ={'a':0,'b':1,'c':2,'d':3,
                  'e':4,'f':5,'g':6,'h':7}
    colsToFile = {v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow*10 + self.endCol
        print(self.moveID)
    
    '''
    Overriding the equals method
    '''
    def __eq__(self,other):
        if isinstance(other,Move): #good practice to check to make sure its a Move class
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFile[c] + self.rowToRanks[r]













