a = input()
t = [0]
for i in range(1, len(a)):
    d = t[i-1]
    while d != 0 and a[i] != a[d]:
        d = t[d-1]
    if a[i] != a[d]:
        t.append(0)
    else:
        t.append(d+1)
print(' '.join(a))
print(*t)
