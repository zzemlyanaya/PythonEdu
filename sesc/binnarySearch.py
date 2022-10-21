def mgcd(a, b, x, y):
    if b == 0:
        return a, x
    x[0], y[0] = y[0], x[0] - y[0]*(a//b)
    x[1], y[1] = y[1], x[1] - y[1]*(a//b)
    a %= b
    return mgcd(b, a, x, y)


def binnary_search(ar, e, lt, rt):
    if lt > rt:
        return False
    else:
        middle = (lt + rt) // 2
        if e == ar[middle]:
            return middle
        elif e > ar[middle]:
            return binnary_search(ar, e, middle + 1, rt)
        else:
            return binnary_search(ar, e, lt, middle - 1)


def bin_search_virt(li, x):
    i = 0
    j = len(li)-1
    while i < j:
        m = int((i+j)/2)
        if x > li[m]:
            i = m+1
        else:
            j = m
    if li[j] == x:
        return j
    else:
        return None


t = list(map(int, input().split()))
n = int(input())
t.sort()
r = bin_search_virt(t, n)
print(r)

