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
            ["--","--","wR","--","--","bB","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions = {'P':self.getPawnMoves,'B':self.getBishopMoves,'K':self.getKingMoves,
                              'N':self.getKnightMoves, 'Q':self.getQueenMoves,'R':self.getRookMoves}
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
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls the appropriate move function based on piece type
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #whte pawn moves
            if self.board[r-1][c] == "--": #check to see if one square above is empty
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c] == "--": #Check to see if first move and if 2 squares above is empty.
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >=0: #Looking to capture to left, but make sure you don't go off board
                if self.board[r-1][c-1][0] == 'b': #enemy capture
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7: #Right capture
                if self.board[r-1][c+1][0] == 'b': #enemy capture
                    moves.append(Move((r,c),(r-1,c+1),self.board))



    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getRookMoves(self,r,c,moves):
        pass

    '''
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def getBishopMoves(self,r,c,moves):
        pass


    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def getKingMoves(self,r,c,moves):
        pass

    '''
    Get all the knight moves for the pawn located at row, col and add these moves to the list
    '''
    def getKnightMoves(self,r,c,moves):
        pass

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def getQueenMoves(self,r,c,moves):
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













