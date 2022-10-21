# n = int(input())
# multiply, cur_index, min_elem = 1000000, 0, 1000000
# delta = 6
# a = [0] * delta
# for i in range(delta):
#     a[i] = int(input())
# for i in range(delta, n):
#     x = int(input())
#     if a[i%6] < min_elem and a[i%6] % 2 != 0:
#         min_elem = a[i%6]
#     if x%2 != 0 and x*min_elem < multiply:
#         multiply = x*min_elem
#     a[i%6] = x
# if multiply % 2 == 0:
#     print(-1)
# else:
#     print(multiply)
n = int(input())
multiply, cur_index, max_elem = 0, 0, 0
s = 8
a = [0]*s
for i in range(s):
    a[i] = int(input())
for i in range(s, n):
    x = int(input())
    if a[cur_index] > max_elem:
        max_elem = a[cur_index]
    if x*max_elem > multiply:
        multiply = x*max_elem
    a[cur_index] = x
    cur_index = (cur_index+1)%s
print(multiply)
