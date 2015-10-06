global counter

def sumUpTo(n):
    if n == 1:
        return 1
    else:
        return n + sumUpTo(n-1)
    
# print (sumUpTo(5))

def alt(n):
    return 1/2* n * (n+1)

# print(alt(5))

def multiply_up(n):
    if n == 0:
        return 1
    else:
        return n * multiply_up(n - 1)

# print(multiply_up(5))

def fib(num):
    global counter
    counter += 1
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fib(num - 1) + fib(num - 2)

def numCalls(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return numCalls(n - 1) + numCalls(n - 2) + 1

def memoized_fib(num, memo_dict):
    global counter
    counter += 1
    if num in memo_dict:
        return memo_dict[num]
    else:
        sum1 = memoized_fib(num - 1, memo_dict)
        sum2 = memoized_fib(num - 2, memo_dict)
        memo_dict[num] = sum1 + sum2
        return sum1 + sum2
"""
for i in range(1, 10):
    global counter
    counter = 0
    print(i, memoized_fib(i, {0 : 0, 1 : 1}), counter, 2*i - 1)
"""

for i in range(5):
    print(i, multiply_up(i))
