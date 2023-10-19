from collections import deque


def has_cycle(graph, start) -> bool:
    global cycle_start
    global cycle_end

    visited, queue = list(), deque()
    queue.append(start)
    while queue:
        next = queue.popleft()
        if next not in visited:
            visited.append(next)
            queue.extend(graph[next])
        else:
            if next == visited[-1]:
                return False
            cycle_start = start
            cycle_end = next
            return True
    return False


def bfs_path(graph, fst, lst):
    queue = deque()
    queue.append((fst, [fst]))
    while queue:
        (v, path) = queue.pop()
        for next in graph[v]:
            if next == lst:
                return path
            else:
                path += [next]
                queue.append((next, path))


with open('in.txt', 'r') as file:
    n = int(file.readline())
    g = dict()
    for i in range(n):
        t = set(map(lambda x: int(x) - 1, file.readline().split()))
        t.remove(-1)
        g[i] = t

    cycle_start = cycle_end = -1

    for i in range(n):
        if has_cycle(g, i):
            break

    res = ''
    if cycle_start != -1:
        res += 'N\n'
        res += ' '.join([str(x + 1) for x in bfs_path(g, cycle_start, cycle_end)])
    else:
        res += 'A'
    with open('out.txt', 'w') as out:
        out.write(res)
