mmax = 0
with open("26.txt") as file:
    n = int(file.readline())
    a = list(map(int, file.readlines()))
    a.sort()
    for i in range(n-1):
        for j in range(i+1, n):
            if a[i]%2 != a[j]%2:
                s = a[i]+a[j]
                if s in a:
                    mmax = max(s, mmax)
print(mmax)