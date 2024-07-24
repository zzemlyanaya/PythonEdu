import math
import matplotlib.pyplot as plt

a = 0
b = 5
h = 0.01
n = int((b - a) / h)


def f(x):
    return math.exp(x) + 2 * math.exp(-x) - 2 * x * (x ** 2 - x + 6)


def f1(x, y, z):
    return z


def f2(x, y, z):
    return y + 2 * x ** 3 - 2 * x ** 2 + 4


def g1(x, u, v):
    return u


def g2(x, u, v):
    return v


def rk4_f(mu, x, y, z):
    global h
    y[0] = mu
    z[0] = 3 * mu - 22
    for i in range(n - 1):
        k1 = h * f1(x[i], y[i], z[i])
        m1 = h * f2(x[i], y[i], z[i])

        k2 = h * f1(x[i] + 0.5 * h, y[i] + 0.5 * k1, z[i] + 0.5 * m1)
        m2 = h * f2(x[i] + 0.5 * h, y[i] + 0.5 * k1, z[i] + 0.5 * m1)

        k3 = h * f1(x[i] + 0.5 * h, y[i] + 0.5 * k2, z[i] + 0.5 * m2)
        m3 = h * f2(x[i] + 0.5 * h, y[i] + 0.5 * k2, z[i] + 0.5 * m2)

        k4 = h * f1(x[i] + h, y[i] + k3, z[i] + m3)
        m4 = h * f2(x[i] + h, y[i] + k3, z[i] + m3)

        y[i + 1] = y[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        z[i + 1] = z[i] + 1 / 6 * (m1 + 2 * m2 + 2 * m3 + m4)
    return y[n - 1] + z[n - 1] - 2 * math.e ** 5 + 402


def rk4_df(x):
    global h
    u = [0] * n
    v = [0] * n
    u[0] = 0
    v[0] = 3
    for i in range(n - 1):
        k1 = h * g1(x[i], u[i], v[i])
        m1 = h * g2(x[i], u[i], v[i])

        k2 = h * g1(x[i] + 0.5 * h, u[i] + 0.5 * k1, v[i] + 0.5 * m1)
        m2 = h * g2(x[i] + 0.5 * h, u[i] + 0.5 * k1, v[i] + 0.5 * m1)

        k3 = h * g1(x[i] + 0.5 * h, u[i] + 0.5 * k2, v[i] + 0.5 * m2)
        m3 = h * g2(x[i] + 0.5 * h, u[i] + 0.5 * k2, v[i] + 0.5 * m2)

        k4 = h * g1(x[i] + h, u[i] + k3, v[i] + m3)
        m4 = h * g2(x[i] + h, u[i] + k3, v[i] + m3)

        u[i + 1] = u[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        v[i + 1] = v[i] + 1 / 6 * (m1 + 2 * m2 + 2 * m3 + m4)
    return u[n - 1] + v[n - 1]


def solve_shooting(x):
    global n
    y = [0] * n
    z = [0] * n
    mu = 0
    d = 1
    c = 1
    while d > 1e-4:
        mu1 = mu - rk4_f(mu, x, y, z) / rk4_df(x)
        d = abs(mu - mu1)
        mu = mu1
        print(c, ' mu = ', mu)
        c += 1
    return y

def p(x):
    return 0


def q(x):
    return -1


def xi(x):
    return 2 * x ** 2 * (x - 1) + 4


def solve_tdma():
    global n
    x = [0.0] * (n + 1)
    y = [0.0] * (n + 1)
    A = [0.0] * (n + 1)
    B = [0.0] * (n + 1)
    C = [0.0] * (n + 1)
    F = [0.0] * (n + 1)
    lam = [0.0] * (n + 1)
    mu = [0.0] * (n + 1)

    for i in range(n + 1):
        x[i] = a + h * i

    for i in range(n):
        A[i] = 1 / (h * h) - p(x[i]) / (2 * h)
        C[i] = 1 / (h * h) + p(x[i]) / (2 * h)
        B[i] = -2 / (h * h) + q(x[i])
        F[i] = xi(x[i])

    B[0] = -h ** 2 - 6 * h - 2
    C[0] = 2
    F[0] = xi(x[0]) * h ** 2 - 44 * h

    B[n] = -h ** 2 - 2 * h - 2
    A[n] = 1
    F[n] = xi(x[n]) * h ** 2 - (2 * math.e ** 5 - 402)

    lam[0] = -C[0] / B[0]
    mu[0] = F[0] / B[0]

    for i in range(1, n + 1):
        lam[i] = -C[i] / (A[i] * lam[i - 1] + B[i])
        mu[i] = (F[i] - A[i] * mu[i - 1]) / (A[i] * lam[i - 1] + B[i])

    y[n] = mu[n]

    for i in range(n - 1, -1, -1):
        y[i] = lam[i] * y[i + 1] + mu[i]

    return y


if __name__ == '__main__':
    x = [a + i * h for i in range(n)]
    f = [f(xi) for xi in x]
    y1 = solve_shooting(x)
    y2 = solve_tdma()[:-1]

    plt.plot(x, f, label='Точное решение')
    plt.plot(x, y1, label='Метод стрельбы (РК-4 & Ньютон)')
    plt.plot(x, y2, label='Метод прогонки (фикт. узел)')
    plt.title('Точность: ' + str(h))
    plt.legend()
    plt.show()
