def game(x, y, depth):
    if x + y >= border or depth > 5:
        return depth == 3 or depth == 5
    if depth%2 ==0:
        return game(x + 2, y, depth + 1) or game(x*2, y, depth + 1) or \
                game(x, y + 2, depth + 1) or game(x, y*2, depth + 1)
    else:
        return game(x + 2, y, depth + 1) and game(x * 2, y, depth + 1) and \
               game(x, y + 2, depth + 1) and game(x, y * 2, depth + 1)



border = 142
for i in range(1, 138 + 1):
    if game(2, i, 1):
        print(i, " ")

print('-------')
def game(x, y, depth):
    if x + y >= border or depth > 3:
        return depth == 3
    if depth%2 ==0:
        return game(x + 2, y, depth + 1) or game(x*2, y, depth + 1) or \
                game(x, y + 2, depth + 1) or game(x, y*2, depth + 1)
    else:
        return game(x + 2, y, depth + 1) and game(x * 2, y, depth + 1) and \
               game(x, y + 2, depth + 1) and game(x, y * 2, depth + 1)



border = 142
for i in range(1, 138 + 1):
    if game(2, i, 1):
        print(i, " ")
