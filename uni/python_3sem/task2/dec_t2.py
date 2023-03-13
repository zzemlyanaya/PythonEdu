import functools
import random

from typing import List
from math import sqrt


def is_simple(n):
    if n % 2 == 0 or n <= 1:
        return False
    sqr = int(sqrt(n)) + 1
    for d in range(3, sqr, 2):
        if n % d == 0:
            return False
    return True


# Модифицируйте код декоратора prime_filter
def prime_filter(func):
    """Дан список целых чисел, возвращайте только простые целые числа"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        res = []
        for i in value:
            if is_simple(i):
                res.append(i)
        return res
    return wrapper


@prime_filter
def numbers(from_num, to_num):
    return [num for num in range(from_num, to_num)]


# вывод для примера
print(numbers(from_num=2, to_num=20)) 
