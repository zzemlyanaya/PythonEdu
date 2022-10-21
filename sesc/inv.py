M = 10**9 + 7


def inv(a):
    w, inv1 = mgcd(a, M)
    return (inv1[0] % M + M) % M


def mgcd_(a, b, x, y):
    if b == 0:
        return a, x
    x[0], y[0] = y[0], x[0] - y[0]*(a//b)
    x[1], y[1] = y[1], x[1] - y[1]*(a//b)
    a %= b
    return mgcd_(b, a, x, y)


def mgcd(a, b):
    return mgcd_(a, b, [1, 0], [0, 1])


n, k = map(int, input().split())
ans = 1
for i in range(1, n + 1):
    ans = (ans*i) % M
for i in range(1, k + 1):
    ans = (ans*inv(i)) % M
for i in range(1, n-k + 1):
    ans = (ans*inv(i)) % M
print(ans)
