import sys

input = sys.stdin.readline

a = []
for i in range(int(input())):
    a.append(int(input()))

a.sort()
print('\n'.join(map(str, a)))