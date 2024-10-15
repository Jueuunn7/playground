import math

def isprime(n):
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True


pr = []

while True:
    p, a = map(int, input().split())

    if p == 0:
        print('\n'.join(pr))
        exit()

    if not isprime(p):
        if pow(a, p, p) == a:
            pr.append('yes')
        else:
            pr.append('no')
    else:
        pr.append('no')


