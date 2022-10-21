msum = 0
count_even, count_uneven = 0, 0
dif_min = []
with open("27-B.txt") as file:
    n = int(file.readline())
    for i in range(n):
        a = sorted(map(int, file.readline().split()))
        msum += a[0]
        if a[0]%2 == 0:
            count_even += 1
        else:
            count_uneven += 1
        if a[1]%2 != a[0]%2:
            dif_min.append(a[1]-a[0])
dif_min.sort()
if count_even > count_uneven:
    if msum%2 != 0:
        print(msum+sum(dif_min[:2]))
    else:
        print(msum)
if count_uneven > count_even:
    if msum%2 == 0:
        print(msum+sum(dif_min[:2]))
    else:
        print(msum)
