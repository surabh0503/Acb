import pygame as p
from GameState import GameState
from Move import Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

def load_images():
    pieces = ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']
    images = {}
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    return images

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = GameState()
    images = load_images()
    running = True
    selected = ()
    playerClicks = []
    validMoves = gs.get_valid_moves()
    print("Valid moves updated. Count:", len(validMoves))


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                print("Mouse click registered")
                loc = p.mouse.get_pos()
                row, col = loc[1]//SQ_SIZE, loc[0]//SQ_SIZE
                if selected == (row, col):
                    selected = ()
                    playerClicks = []
                else:
                    selected = (row, col)
                    playerClicks.append(selected)
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print("Attempting move:", move.get_chess_notation())
                    print("Valid moves:")
                    for m in validMoves:
                            print(m.get_chess_notation())
                    if move in validMoves:
                        gs.make_move(move)
                        validMoves = gs.get_valid_moves()
                    selected = ()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    validMoves = gs.get_valid_moves()

        draw_game(screen, gs, images)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_game(screen, gs, images):
    draw_board(screen)
    draw_pieces(screen, gs.board, images)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, colors[(r+c)%2], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, images):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
