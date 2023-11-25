def dfs(C, F, s, t, n):
    stack = [s]
    paths = {s: []}
    if s == t:
        return paths[s]
    while stack:
        u = stack.pop()
        for v in range(n):
            if (C[u][v] - F[u][v] > 0) and v not in paths:
                paths[v] = paths[u] + [(u, v)]
                if v == t:
                    return paths[v]
                stack.append(v)
    return None


def max_flow(C, s, t, n):
    F = [[0] * n for _ in range(n)]
    maxflow = 0

    path = dfs(C, F, s, t, n)
    while path is not None:
        flow = min(C[u][v] - F[u][v] for u, v in path)
        maxflow += flow
        for u, v in path:
            F[u][v] += flow
            F[v][u] -= flow
        path = dfs(C, F, s, t, n)
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
