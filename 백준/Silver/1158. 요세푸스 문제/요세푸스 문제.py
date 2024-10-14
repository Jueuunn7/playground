import sys
from collections import deque

input = sys.stdin.readline
ans = deque()

L, M = map(int, input().split())

a = [i for i in range(1, L+1)]


for _ in range(L):
    for _ in range(M):
        q = a.pop(0)
        a.append(q)

    q = a.pop()
    ans.append(q)

print('<'+', '  .join(map(str, ans))+'>')