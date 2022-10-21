def gcd(a, b):
    if b <= 0:
        return a
    else:
        return gcd(b, a%b)


a, b, c, d = map(int, input().split(" "))
up = a*d + b*c
down = b*d
gCD = gcd(up, down)
if up == 0:
    print(0)
    exit()
if gcd == 1:
    print(str(up)+"/"+str(down))
else:
    up //= gCD
    down //= gCD
    if up//down != 0:
        print(up//down, str(up%down)+"/"+str(down))
    else:
        print(str(up)+"/"+str(down))