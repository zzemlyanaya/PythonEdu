import math
import matplotlib.pyplot as plt

ax = 0
bx = 5
h = 0.01
N = int((bx - ax) / h)


def f(x):
    return math.exp(x) + 2 * math.exp(-x) - 2 * x * (x ** 2 - x + 6)


def y_an(x):
    return math.exp(x) + 2 * math.exp(-x) - 2 * x * (x ** 2 - x + 6)


def p(x):
    return 0


def q(x):
    return -1


def f1(x):
    return 2 * x ** 2 * (x - 1) + 4


x = [0.0] * (N + 1)
y = [0.0] * (N + 1)
A = [0.0] * (N + 1)
B = [0.0] * (N + 1)
C = [0.0] * (N + 1)
F = [0.0] * (N + 1)
aa = [0.0] * (N + 1)
bb = [0.0] * (N + 1)

h = (bx - ax) / N

for i in range(N + 1):
    x[i] = ax + h * i

for i in range(N):
    A[i] = 1 / (h * h) - p(x[i]) / (2 * h)
    C[i] = 1 / (h * h) + p(x[i]) / (2 * h)
    B[i] = -2 / (h * h) + q(x[i])
    F[i] = f1(x[i])

B[0] = -h ** 2 - 6 * h - 2
C[0] = 2
F[0] = f1(x[0]) * h ** 2 - 44*h

B[N] = -h ** 2 - 2 * h - 2
A[N] = 1
F[N] = f1(x[N])*h**2 - (2 * math.e ** 5 - 402)

aa[0] = -C[0] / B[0]
bb[0] = F[0] / B[0]

for i in range(1, N + 1):
    aa[i] = -C[i] / (A[i] * aa[i - 1] + B[i])
    bb[i] = (F[i] - A[i] * bb[i - 1]) / (A[i] * aa[i - 1] + B[i])

y[N] = (F[N] - bb[N - 1] * A[N]) / (B[N] + aa[N - 1] * A[N])

for i in range(N - 1, -1, -1):
    y[i] = aa[i] * y[i + 1] + bb[i]

f = [f(xi) for xi in x]

plt.plot(x, f, label='Точное решение')
plt.plot(x, y, label='Прогонка')
plt.legend()
plt.show()
