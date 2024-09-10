import sys

input = sys.stdin.readline
que = []
for _ in range(int(input())):
    op = input().split()
    try:
        if op[0] == "1":
            que.append(int(op[1]))

        elif op[0] == "2":
            print(que.pop(-1))
        
        elif op[0] == "3":
            print(len(que))

        elif op[0] == "4":
            print(int(len(que) == 0))

        elif op[0] == "5":
            print(que[-1])

    except:
        print(-1)

