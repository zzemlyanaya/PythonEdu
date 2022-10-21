import random


def bp(a, n):
    if n == 0:
        return 1
    else:
        ans = bp(a, n//2)
        ans *= ans
        if n % 2 != 0:
            ans *= a
        return ans


def quick_sort(ar, fst, lst):
    if fst >= lst:
        return
    i, j = fst, lst
    p = ar[random.randint(fst, lst)]
    while i <= j:
        while ar[i] < p:
            i += 1
        while ar[j] > p:
            j -= 1
        if i <= j:
            ar[i], ar[j] = ar[j], ar[i]
            i += 1
            j -= 1
            quick_sort(ar, fst, j)
            quick_sort(ar, i, lst)


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    l = merge_sort(a[:mid])
    r = merge_sort(a[mid:])
    return merge(l, r)


def merge(l, r):
    res = []
    i, j = 0, 0
    while i < len(l) and j < len(r):
        if l[i] < r[j]:
            res.append(l[i])
            i += 1
        else:
            res.append(r[j])
            j += 1
    res += l[i:] + r[j:]
    return res


t = list(map(int, input().split()))
s = input("Введите 1 для сортировки Хоара и 2 для сортировки слиянием\n")
if s == "1":
    print(quick_sort(t, 0, len(t)-1))
elif s == "2":
    print(merge_sort(t))
else:
    print("Неизвестная команда. Выход из системы")