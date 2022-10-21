def game(x, y, d):
    global depth, border
    if x + y >= border:
        return False
    elif d == depth:
        return True
    else:
        return not(game(x+1, y, d+1) and game(x*4, y, d+1) and game(x, y+1, d+1) and game(x, y*4, d+1))


depth, border = map(int, input().split())
for i in range(1, border):
    if depth & 1:
        if game(i, 9, 0):
            print(i, end=" ")
    else:
        if not game(i, 9, 0):
            print(i, end=" ")