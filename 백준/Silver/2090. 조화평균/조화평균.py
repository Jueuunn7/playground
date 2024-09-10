from fractions import Fraction
co, A = int(input()), input().split()
if co == 1:print(f"{A[0]}/1")
else:print(Fraction(1, sum([Fraction(1, int(A[i])) for i in range(co)])))