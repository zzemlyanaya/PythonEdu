INFINITY = 10**7


def dfs(v):
    visited[v] = 1
    for z in adj_list[v]:
        if visited[z] == 0:
            dfs(z)
        elif visited[z] == 1:
            print("No")
            exit()
    visited[v] = 2
    ans.append(v + 1)


def bfs(start):
    far[start] = 0
    queue = [start]
    q_start = 0
    while q_start < len(queue):
        u = queue[q_start]
        q_start += 1
        for v in adj_list[u]:
            if far[v] == -1:
                far[v] = far[u] + 1
                prev[v] = u
                queue.append(v)


def print_path(start, last):
    path = ""
    while last != start:
        path += str(last + 1) + " "
        last = prev[last]
    path += str(last + 1)
    print(*list(reversed(path.split(" "))))


def topological_sort():
    for t in range(n):
        if not visited[t]:
            dfs(t)
    ans.reverse()


def dijkstra(s):
    dist[s] = 0
    prev[s] = 0
    for count in range(n):
        u = min_distance()
        visited[u] = 1
        for v in range(n):
            if graph[u][v] >= 0 and visited[v] == 0 and dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]
                prev[v] = u


def min_distance():
    min = INFINITY
    min_index = 0
    for v in range(n):
        if dist[v] < min and visited[v] == 0:
            min = dist[v]
            min_index = v
    return min_index


n, m = map(int, input().split())
ans = []
visited = [0] * n
adj_list = [[] for x in range(n * 2)]
prev = []
far = []
dist = [INFINITY]*n
graph = [[]]
