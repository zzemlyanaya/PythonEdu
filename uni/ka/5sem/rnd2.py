from collections import deque


def find_max_flow(capacity, source, sink):
    n = len(capacity)

    max_flow = 0
    flow = [[0] * n for _ in range(n)]
    residual_capacity = [row[:] for row in capacity]

    while True:
        pred = bfs(residual_capacity, flow, source, sink)
        if pred[sink] == -1:
            break

        v = sink
        bottleneck = float('+inf')
        while v != source:
            u = pred[v]
            if residual_capacity[u][v] > 0: # если направление прямое
                edge_capacity = residual_capacity[u][v]
            else: # если обратное направление
                edge_capacity = flow[v][u]
            bottleneck = min(bottleneck, edge_capacity)
            v = u

        v = sink
        while v != source:
            u = pred[v]
            if residual_capacity[u][v] > 0:
                flow[u][v] += bottleneck
                residual_capacity[u][v] -= bottleneck
            else:
                flow[v][u] -= bottleneck # отменяем поток, который идет не по пути цепи.
                residual_capacity[u][v] += bottleneck
            v = u

        max_flow += bottleneck

    return max_flow, flow

def bfs(residual_capacity, flow, source, sink):
    n = len(residual_capacity)
    visited = [False] * n
    pred = [-1] * n

    visited[source] = True
    queue = deque()
    queue.append(source)

    while queue:
        u = queue.popleft()
        for v in range(len(residual_capacity[u])):
            if not visited[v] and (residual_capacity[u][v] or flow[v][u]):
                visited[v] = True
                pred[v] = u
                if v == sink:
                    return pred
                queue.append(v)
    return pred


with open("in.txt", "r") as f:
    n = int(f.readline())
    capacity = [list(map(int, f.readline().split())) for _ in range(n)]
    source = int(f.readline()) - 1
    sink = int(f.readline()) - 1


max_flow, flow = find_max_flow(capacity, source, sink)

with open("out.txt", "w") as f:
    for row in flow:
        f.write(' '.join(map(str, row)) + '\n')
    f.write(str(max_flow) + '\n')