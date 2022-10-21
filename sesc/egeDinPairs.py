d = 126
r = [0] * d
fst = 0
scnd = 0
n = int(input())
for i in range(n):
    a = int(input())
    p = a % d
    if r[(d - p) % d] > a and r[(d - p) % d] + a > fst + scnd:
        fst = r[(d - p) % d]
        scnd = a
    if a > r[p]:
        r[p] = a
if fst + scnd != 0:
    print(fst, scnd)
else:
    print(-1)

