import random
import curses

def draw_board(win):
    for i in range(1, height - 1):
        win.addch(i, 0, '|')
        win.addch(i, width - 1, '|')

    for j in range(1, width - 1):
        win.addch(height - 1, j, '_')

def draw_tetromino(win, tetromino):
    for i in range(4):
        for j in range(4):
            if tetromino[i][j] == 'X':
                win.addch(y + i, x + 2 * j, '*')

def clear_tetromino(win, tetromino):
    for i in range(4):
        for j in range(4):
            if tetromino[i][j] == 'X':
                win.addch(y + i, x + 2 * j, ' ')

def rotate_tetromino(tetromino):
    return [list(row) for row in zip(*reversed(tetromino))]

def can_move(matrix, tetromino, tetromino_x, tetromino_y):
    for i in range(4):
        for j in range(4):
            if tetromino[i][j] == 'X' and matrix[tetromino_y + i][tetromino_x + j * 2] != ' ':
                return False
    return True

def merge_tetromino(matrix, tetromino, tetromino_x, tetromino_y):
    for i in range(4):
        for j in range(4):
            if tetromino[i][j] == 'X':
                matrix[tetromino_y + i][tetromino_x + j * 2] = '*'

def check_rows(matrix):
    rows_to_clear = []
    for i in range(height - 2, 0, -1):
        if all(matrix[i][j * 2] == '*' for j in range(1, width // 2 - 1)):
            rows_to_clear.append(i)
    return rows_to_clear

def clear_rows(matrix, rows):
    for row in rows:
        del matrix[row]
        matrix.insert(1, [' '] * (width - 2))

def tetris_game(stdscr):
    global x, y, tetromino, tetromino_index, height, width

    curses.curs_set(0)
    stdscr.timeout(100)

    height, width = stdscr.getmaxyx()

    matrix = [[' '] * (width - 2) for _ in range(height - 1)]

    tetrominoes = [
        [['X', 'X', 'X', 'X']],
        [['X', 'X', 'X'], [' ', 'X', ' ']],
        [['X', 'X', 'X'], ['X', ' ', ' ']],
        [['X', 'X'], ['X', 'X']],
        [['X', 'X', ' '], [' ', 'X', 'X']],
        [[' ', 'X', 'X'], ['X', 'X']]
    ]

    x = width // 4
    y = 0
    tetromino_index = random.randint(0, len(tetrominoes) - 1)
    tetromino = tetrominoes[tetromino_index]

    while True:
        stdscr.clear()

        draw_board(stdscr)
        draw_tetromino(stdscr, tetromino)

        if can_move(matrix, tetromino, x, y + 1):
            y += 1
        else:
            merge_tetromino(matrix, tetromino, x, y)
            cleared_rows = check_rows(matrix)
            if cleared_rows:
                clear_rows(matrix, cleared_rows)
            x = width // 4
            y = 0
            tetromino_index = random.randint(0, len(tetrominoes) - 1)
            tetromino = tetrominoes[tetromino_index]

        for i, row in enumerate(matrix):
            for j in range(len(row)):
                if matrix[i][j] == '*':
                    stdscr.addch(i + 1, j + 1, '*')

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT and can_move(matrix, tetromino, x - 2, y):
            x -= 2
        elif key == curses.KEY_RIGHT and can_move(matrix, tetromino, x + 2, y):
            x += 2
        elif key == curses.KEY_DOWN and can_move(matrix, tetromino, x, y + 1):
            y += 1
        elif key == curses.KEY_UP:
            rotated_tetromino = rotate_tetromino(tetromino)
            if can_move(matrix, rotated_tetromino, x, y):
                clear_tetromino(stdscr, tetromino)
                tetromino = rotated_tetromino

if __name__ == "__main__":
    curses.wrapper(tetris_game)
