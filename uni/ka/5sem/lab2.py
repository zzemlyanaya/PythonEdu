def breadth_first_search(graph: list, source: int, sink: int, parents: list) -> bool:

    visited = [False] * len(graph)  # Mark all nodes as not visited
    queue = []  # breadth-first search queue

    # Source node
    queue.append(source)
    visited[source] = True

    while queue:
        u = queue.pop(0)  # Pop the front node
        # Traverse all adjacent nodes of u
        for ind, node in enumerate(graph[u]):
            if visited[ind] is False and node > 0:
                queue.append(ind)
                visited[ind] = True
                parents[ind] = u
    return visited[sink]


def ford_fulkerson(graph: list, source: int, sink: int):

    # This array is filled by breadth-first search and to store path
    parent = [-1] * (len(graph))
    max_flow = 0

    # While there is a path from source to sink
    while breadth_first_search(graph, source, sink, parent):
        path_flow = int(1e9)  # Infinite value
        s = sink

        while s != source:
            # Find the minimum value in the selected path
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = sink

        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]

    return max_flow, graph


with open('in.txt', 'r') as file:
    N = int(file.readline())
    graph = []
    for _ in range(N):
        row = list(map(int, file.readline().split()))
        graph.append(row)
    source = int(file.readline()) - 1
    target = int(file.readline()) - 1

    max_flow, graph = ford_fulkerson(graph, source, target)

    with open('out.txt', 'w') as out:
        for row in graph:
            out.write(' '.join(map(str, row)) + '\n')
        out.write(str(max_flow))