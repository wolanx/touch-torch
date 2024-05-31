def _get_next(m, x, y):
    for next_y in range(y + 1, 9):
        if m[x][next_y] == 0:
            return x, next_y
    for next_x in range(x + 1, 9):
        for next_y in range(0, 9):
            if m[next_x][next_y] == 0:
                return next_x, next_y
    return -1, -1


def _value(m, x, y):
    i, j = x // 3, y // 3
    grid = [m[i * 3 + r][j * 3 + c] for r in range(3) for c in range(3)]
    v = set(range(1, 10)) - set(grid) - set(m[x]) - set(list(zip(*m))[y])
    return list(v)


def sudoku_init(m):
    for x in range(9):
        for y in range(9):
            if m[x][y] == 0:
                return x, y
    return -1, -1


def sudoku_run(m, x=0, y=0):
    if x == 9:
        return True
    if y == 9:
        return sudoku_run(m, x + 1, 0)
    if m[x][y] != 0:
        return sudoku_run(m, x, y + 1)
    for v in _value(m, x, y):
        m[x][y] = v
        if sudoku_run(m, x, y + 1):
            return True
        m[x][y] = 0
    return False
