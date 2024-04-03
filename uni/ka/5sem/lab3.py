def find_groups(board):
    groups = []
    visited = set()

    def dfs(row, col, color, group):
        if (
            1 <= row <= 8
            and 1 <= col <= 8
            and board[row - 1][col - 1] == color
            and (row, col) not in visited
        ):
            visited.add((row, col))
            group.append((row, col))

            dfs(row - 1, col, color, group)
            dfs(row + 1, col, color, group)
            dfs(row, col - 1, color, group)
            dfs(row, col + 1, color, group)

    for i in range(8):
        for j in range(8):
            if board[i][j] != '.' and (i + 1, j + 1) not in visited:
                new_group = []
                dfs(i + 1, j + 1, board[i][j], new_group)
                groups.append(new_group)

    return groups


def possible_moves(color, board):
    opponent_color = "W" if color == "B" else "B"
    opponent_groups = find_groups(board)

    best_moves = []
    max_captured = 0

    for i in range(8):
        for j in range(8):
            if board[i][j] == ".":
                temp_board = [row[:] for row in board]
                temp_board[i][j] = color

                captured = 0
                for group in opponent_groups:
                    if all(cell in temp_board for cell in group):
                        captured += len(group)

                if captured > max_captured:
                    max_captured = captured
                    best_moves = [(i + 1, j + 1)]
                elif captured == max_captured:
                    best_moves.append((i + 1, j + 1))

    return best_moves if best_moves else ["N"]


white_stones = []
black_stones = []

(row, col) = map(int, input().split(" "))
while (row, col) != (0, 0):
    white_stones.append((row, col))
    (row, col) = map(int, input().split(" "))

(row, col) = map(int, input().split(" "))
while (row, col) != (0, 0):
    black_stones.append((row, col))
    (row, col) = map(int, input().split(" "))

board = [["." for _ in range(8)] for _ in range(8)]

for row, col in white_stones:
    board[row - 1][col - 1] = "W"

for row, col in black_stones:
    board[row - 1][col - 1] = "B"

white_moves = possible_moves("W", board)
black_moves = possible_moves("B", board)

print(" ".join(map(str, white_moves)))
print(" ".join(map(str, black_moves)))

# 1 1
# 1 2
# 3 3
# 3 1
# 4 2
# 5 5
# 2 7
# 1 8
# 2 3
# 1 6
# 3 8
# 1 4
# 0 0
# 2 1
# 2 2
# 3 2
# 5 4
# 4 5
# 6 5
# 2 6
# 1 3
# 1 7
# 2 8
# 0 0
#
# N
# 1 5
# 3 1
# 3 7
# 5 6