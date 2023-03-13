#  Copyright (c) Evgeniya Zemlyanaya @zzemlyanaya 14/10/2022

from collections import deque


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for v in graph[start] - visited:
        dfs(graph, v, visited)
    return visited


def dfs_path(graph, fst, lst):
    stack = deque()
    stack.append((fst, [fst]))
    while stack:
        (v, path) = stack.popleft()
        for next in graph[v] - set(path):
            if next == lst:
                return path + [next]
            else:
                stack.append((next, path + [next]))


def bfs(graph, start):
    visited, queue = set(), deque()
    queue.append(start)
    while queue:
        v = queue.popleft()
        if v not in visited:
            visited.add(v)
            queue.extend(graph[v] - visited)
    return visited


def bfs_path(graph, fst, lst):
    queue = deque()
    queue.append((fst, [fst]))
    while queue:
        (v, path) = queue.pop()
        for next in graph[v] - set(path):
            if next == lst:
                return path + [next]
            else:
                queue.append((next, path + [next]))


g = {
    1: {2, 3},
    2: {1, 3, 4, 5},
    3: {1, 2, 5, 7,  8},
    4: {2, 5},
    5: {3, 4, 6},
    6: set(),
    7: {3, 8},
    8: {3, 7},
}


res = list(dfs_path(g, 1, 7))
print('here is dfs_path result from vertex 1 to 6 ', res)
res = list(bfs_path(g, 1, 7))
print('here is bfs_path result from vertex 1 to 6 ', res)
