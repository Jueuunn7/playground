import sys
from collections import deque

input = sys.stdin.readline
que = deque()
for _ in range(int(input())):
    op = input().split()
    try:
        if op[0] == "push":
            que.append(int(op[1]))

        elif op[0] == "pop":
            print(que.popleft())
        
        elif op[0] == "size":
            print(len(que))

        elif op[0] == "empty":
            print(int(len(que) == 0))

        elif op[0] == "front":
            print(que[0])

        elif op[0] == "back":
            print(que[-1])
    except:
        print(-1)