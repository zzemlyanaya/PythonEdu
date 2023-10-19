class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)


def get_min_dist(dist, n, MST):
    min_dist = 1e9
    for v in range(n):
        if dist[v] < min_dist and not MST[v]:
            min_dist = dist[v]
            min_index = v
    return min_index


with open('in.txt') as f:
    n = int(f.readline())
    points = []
    for i in range(n):
        x, y = map(int, f.readline().split())
        points.append(Point(x, y))

    graph = [[points[i].dist(points[j]) for j in range(n)] for i in range(n)]
    dist = [1e9] * n
    parent = [None] * n
    MST = [False] * n

    dist[0] = 0
    parent[0] = -1
    weight = 0

    # solve
    for _ in range(n):
        u = get_min_dist(dist, n, MST)
        MST[u] = True

        for v in range(n):
            if 0 < graph[u][v] < dist[v] and not MST[v]:
                dist[v] = graph[u][v]
                parent[v] = u

        weight += dist[u]

    # print
    adj_list = [set() for _ in range(n)]
    for i in range(1, n):
        adj_list[i].add(parent[i])
        adj_list[parent[i]].add(i)

    with open('out.txt', 'w') as out:
        for i in range(n):
            out.write(' '.join(map(lambda x: str(x + 1), adj_list[i])))
            out.write(' 0')
            out.write('\n')
        out.write(str(weight))
