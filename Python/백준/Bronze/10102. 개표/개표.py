a = input()
x = input()

c = x.count('A')
b = x.count('B')
if (c == b):
    print("Tie")
elif (c > b):
    print("A")
else:
    print("B")