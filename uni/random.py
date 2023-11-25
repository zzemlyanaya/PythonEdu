def compute(a, b):
    counter = 0
    if a == b:
        return 1
    if b == 0:
        return 0
    while a % b == 0:
        counter += 1
        a //= b
    return counter