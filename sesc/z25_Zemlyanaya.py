from math import sqrt


def is_simple(n):
    if n % 2 == 0 or n <= 1:
        return False
    sqr = int(sqrt(n)) + 1
    for d in range(3, sqr, 2):
        if n % d == 0:
            return False
    return True


def ok(n):
    res = []
    for d in range(2, int(n**0.5)+1):
        if d > 3:
            return False
        p = 0
        while n%d == 0:
            p += 1
            n //= d
        res.append(d)
    if len(res) == 2 and res[0]%2 == 0 and res[1]%2 == 1:
        return True
    else:
        return False


def sum_fact(n):
    return sum(i for i in range(1, n) if n % i == 0)


res = []
for m in range(0, 30, 2):
    for n in range(1, 30, 2):
        if 200000000 <= 2**m * 3**n <= 400000000:
            res.append(2**m*3**n)
print(*sorted(res))
