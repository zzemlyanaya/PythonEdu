from collections import deque


def bfs(C, F, s, t, n):
    queue = deque([s])
    paths = {s: []}

    while queue:
        u = queue.popleft()

        if u == t:
            return paths[u]

        for v in range(n):
            if (C[u][v] - F[u][v] > 0) and v not in paths:
                paths[v] = paths[u] + [(u, v)]
                queue.append(v)

    return None


def max_flow(C, s, t, n):
    F = [[0] * n for _ in range(n)]
    R = [row[:] for row in C]
    maxflow = 0
    flow = float('+inf')

    path = bfs(R, F, s, t, n)
    while path is not None:
        for u, v in path:
            if R[u][v] > 0:
                e = R[u][v]
            else:
                e = F[u][v]

            flow = min(flow, e)

        maxflow += flow
        for u, v in path:
            if R[u][v] > 0:
                F[u][v] += flow
                R[u][v] -= flow
            else:
                F[u][v] -= flow
                R[u][v] += flow
        path = bfs(C, F, s, t, n)
    return F, maxflow


with open('in.txt', 'r') as file:
    N = int(file.readline())
    graph = []
    for _ in range(N):
        row = list(map(int, file.readline().split()))
        graph.append(row)
    source = int(file.readline()) - 1
    target = int(file.readline()) - 1

    g, max_flow = max_flow(graph, source, target, N)

    with open('out.txt', 'w') as out:
        for row in g:
            out.write(' '.join(map(str, row)) + '\n')
        out.write(str(max_flow))
