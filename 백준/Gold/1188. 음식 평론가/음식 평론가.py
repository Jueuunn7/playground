import math

a = list(map(int, input().split()))

print(a[1] - math.gcd(a[0], a[1]))