class GameState():
    def __init__(self):
        #-board is 8x8 2d list
        #-first character represents color of piece, b or w
        #-the second character represents type of piece
        #  R=Rook,N=Knight,B=Bishop,Q=Queen,K=King,P=Pawn
        self.board = [
            # ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            # ["--","--","bR","--","--","--","--","--"],
            # ["--","--","--","--","--","--","--","--"],
            # ["--","--","--","wB","bB","--","--","--"],
            # ["--","--","--","--","--","--","--","--"],
            # ["--","--","--","--","--","--","--","--"],
            # ["wR","--","--","--","--","--","--","--"],
            # ["wR","wN","wB","wQ","wK","wB","wN","wR"]

            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
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
        else: #black pawn moves
            if self.board[r+1][c] == "--": #check to see if one square below is empty
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c] == "--": #check to see if the square 2 below is empty
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0: #capture to left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7: #capture to right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getUniversalMoves(self,r,c,moves,directions):
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8): #checking 7 moves in this particular direction
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space, valid and keep going
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece, valid, and must stop here
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: #friendly piece, invalid, must stop here
                        break
                else: #off board, invalid, must stop here
                    break

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getRookMoves(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1)) #up,left,down,right
        self.getUniversalMoves(r,c,moves,directions)

    '''
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def getBishopMoves(self,r,c,moves):
        directions=((-1,-1),(-1,1),(1,-1),(1,1)) #4 diagonals
        self.getUniversalMoves(r,c,moves,directions)

    '''
    Get all the knight moves for the pawn located at row, col and add these moves to the list
    '''
    def getKnightMoves(self,r,c,moves):
        lmoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #L shaped move in all directions
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in lmoves:
            endRow=r+m[0]
            endCol=c+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0] != allyColor: #valid move,if it isn't ally then its either enemy or empty
                    moves.append(Move((r,c),(endRow,endCol),self.board))



    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor='w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow=r+kingMoves[i][0]
            endCol=c+kingMoves[i][1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not ally piece (empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def getQueenMoves(self,r,c,moves):
        #queen can do same moves as rooks and bishops
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

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

    def printMove(self):
        print('startRow:',self.startRow,'startCol:',self.startCol,'endRow:',self.endRow,'endCol:',self.endCol)













