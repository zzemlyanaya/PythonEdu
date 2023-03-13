import random
from math import sqrt


def is_simple(n):
    if n % 2 == 0 or n <= 1:
        return False
    sqr = int(sqrt(n)) + 1
    for d in range(3, sqr, 2):
        if n % d == 0:
            return False
    return True


def simple_generator(n):
    for i in range(n):
        if is_simple(i):
            yield i


simple_gen_instance = simple_generator(10**7+3)
while input() != '':
    print(next(simple_gen_instance))
