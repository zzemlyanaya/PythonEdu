d = dict()
alp = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
mmax = 0
with open('24.txt') as file:
    a = file.readlines()
    for s in a:
        if s.count('A') >= 25:
            continue
        else:
            for i in alp:
                if s.count(i) > 1:
                    dist = s.rfind(i) - s.find(i)
                    mmax = max(mmax, dist)
print(mmax)


