import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 #400 is another option can play around 
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionay of images. This will be called esactly once in main
'''
def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))

'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = () #(row,col)
    playerClicks = [] #keep track of player clicks, 2 tuples

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #user clicked same square twice
                    sqSelcted=()#unselect it
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    #reset moves
                    sqSelected = ()
                    playerClicks=[]
            #keyboard handler
            elif e.type == p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undoMove()
                    moveMade = True

        # if moveMade:
        #     validMoves = gs.getValidMoves()
        #     moveMade = False

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current game state.
'''
def drawGameState(screen,gs):
    ##Order matters, board should be draw first then pieces
    drawBoard(screen) #draw squares on the board
    drawPieces(screen,gs.board) #draw piece

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors= [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == "__main__":
    main()