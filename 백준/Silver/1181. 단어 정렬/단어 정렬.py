string = []

for _ in range(int(input())):
    string.append(input())

l = list(set(string))
l.sort(key=lambda x: (len(x), x))
print('\n'.join(l))