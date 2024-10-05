import sys

input = sys.stdin.readline

input()

q = list(map(int, input().split()))
w = list(map(int, input().split()))

a = q + w

a.sort()

print(' '.join(map(str, a)))