a = []
for i in range(int(input())):
    f = input().split()
    a.append([int(f[0]), f[1]])

a.sort(key=lambda x: x[0])

for i in a:
    print(f'{i[0]} {i[1]}')