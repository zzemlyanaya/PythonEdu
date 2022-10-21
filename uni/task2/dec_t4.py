from numpy import random
import time
import functools


# Напишите декоратор retry:
#
# декоратор вызовает функцию, которая возвращает True/False для индикации успешного или неуспешного выполнения функции.
# При сбое декоратор должен подождать и повторить попытку выполнения функции.
# При повторных неудачах декоратор должен ждать дольше между каждой последующей попыткой.
# Если у декоратора заканчиваются попытки, он сдается и возвращает исключе


def retry(times, sleep, sleep_exp=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            sleep_time = sleep
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    time.sleep(sleep_time)
                    sleep_time *= sleep_exp
                    attempt += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator


@retry(times=3, sleep=1)
def foo1(number):
    if number % 2 == 0:
        raise ValueError('Some error')
    else:
        print("OK")


foo1(3)
foo1(4)