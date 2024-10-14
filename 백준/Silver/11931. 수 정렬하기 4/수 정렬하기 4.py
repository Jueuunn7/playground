import sys

l = []

input = sys.stdin.readline

N = int(input())

for i in range(N):
    l.append(int(input()))

l.sort(reverse=True)

print('\n'.join(map(str, l)))