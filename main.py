import pygame, random, sys

# --- Paramètres du jeu ---
CELL_SIZE = 30
COLS, ROWS = 10, 20
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
WINDOW_SCALE = 1.5
FPS = 60  # nombre de frames par seconde

# --- Couleurs ---
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 0, 0)
]

# --- Formes Tetris ---
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0],
     [1, 1, 1]],     # J
    [[0, 0, 1],
     [1, 1, 1]],     # L
    [[1, 1],
     [1, 1]],        # O
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[0, 1, 0],
     [1, 1, 1]],     # T
    [[1, 1, 0],
     [0, 1, 1]]      # Z
]

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def check_collision(board, piece, offset_x=0, offset_y=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece.x + x + offset_x
                new_y = piece.y + y + offset_y
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return True
                if new_y >= 0 and board[new_y][new_x]:
                    return True
    return False

def merge_piece(board, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell and piece.y + y >= 0:
                board[piece.y + y][piece.x + x] = piece.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    return new_board, cleared

def draw_board(screen, board, piece):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            color = cell if cell else GRAY
            pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, ((piece.x+x)*CELL_SIZE, (piece.y+y)*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

def main():
    pygame.init()
    pygame.mixer.init()

    # Charger et jouer la musique en boucle
    pygame.mixer.music.load("tetris.mp3")
    pygame.mixer.music.play(-1)  # -1 signifie boucle infinie
    screen = pygame.display.set_mode((int(WIDTH*WINDOW_SCALE), int(HEIGHT*WINDOW_SCALE)))
    pygame.display.set_caption("Tetris macOS")
    clock = pygame.time.Clock()

    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    piece = Piece(random.choice(SHAPES))

    fall_time = 0
    fall_speed = 0.5  # descend toutes les 0.5 secondes

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # temps écoulé en secondes
        fall_time += dt

        if fall_time >= fall_speed:
            piece.y += 1
            if check_collision(board, piece):
                piece.y -= 1
                merge_piece(board, piece)
                board, _ = clear_lines(board)
                piece = Piece(random.choice(SHAPES))
                if check_collision(board, piece):
                    running = False
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, piece, offset_x=-1):
                        piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, piece, offset_x=1):
                        piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, piece, offset_y=1):
                        piece.y += 1
                elif event.key == pygame.K_UP:
                    piece.rotate()
                    if check_collision(board, piece):
                        for _ in range(3):
                            piece.rotate()  # rotation inverse

        screen.fill(BLACK)
        draw_board(screen, board, piece)
        pygame.display.update()

    print("Game Over!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
