#  Copyright (c) Evgeniya Zemlyanaya @zzemlyanaya 14/10/2022


# def dfs_paths(graph, start, goal):
#     stack = [(start, [start])]
#     while stack:
#         (vertex, path) = stack.pop()
#         for next in graph[vertex] - set(path):
#             if next == goal:
#                 yield path + [next]
#             else:
#                 stack.append((next, path + [next]))

# def bfs_paths(graph, start, goal):
#     queue = [(start, [start])]
#     while queue:
#         (vertex, path) = queue.pop(0)
#         for next in graph[vertex] - set(path):
#             if next == goal:
#                 yield path + [next]
#             else:
#                 queue.append((next, path + [next]))
