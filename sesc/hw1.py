from math import sqrt


def is_simple(n):
    if n % 2 == 0 or n <= 1:
        return False
    root = int(sqrt(n)) + 1
    for d in range(3, root, 2):
        if n % d == 0:
            return False
    return True


def nums_sum(n):
    return sum(list(map(int, list(str(n)))))


def is_ok(n):
    dels = []
    for d in range(3, int(n**0.5)+1, 2):
        if n%d == 0:
            dels.append(d)
            if n//d != d and n//d % 2 != 0:
                dels.append(n//d)
    if len(dels) == 5:
        return max(dels)
    else:
        return False


i = 1
while True:
    dels = [1]
    for d in range(2, int(i**0.5)+1):
        if i%d == 0:
            dels.append(i)
            if i//d != d:
                dels.append(i//d)
        if len(dels) > 1600:
            break
    if len(dels) == 1600:
        print(i, max(dels))
        break