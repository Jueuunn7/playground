input()

a = list(map(int, input().split()))

a = set(a)
a = list(a)

a.sort()

print(' '.join(map(str, a)))