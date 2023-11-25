from collections import defaultdict


class Graph:

    def __init__(self, graph):
        self.graph = graph
        self. ROW = len(graph)


    # Using BFS as a searching algorithm
    def searching_algo_BFS(self, s, t, parent):

        visited = [False] * (self.ROW)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Applying fordfulkerson algorithm
    def ford_fulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0

        while self.searching_algo_BFS(source, sink, parent):

            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            max_flow += path_flow

            # Updating the residual values of edges
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return self.graph, max_flow


with open('in.txt', 'r') as file:
    N = int(file.readline())
    graph = []
    for _ in range(N):
        row = list(map(int, file.readline().split()))
        graph.append(row)
    source = int(file.readline()) - 1
    target = int(file.readline()) - 1

    g = Graph(graph)

    max_flow = g.ford_fulkerson(source, target)

    with open('out.txt', 'w') as out:
        for row in g.graph:
            out.write(' '.join(map(str, row)) + '\n')
        out.write(str(max_flow))