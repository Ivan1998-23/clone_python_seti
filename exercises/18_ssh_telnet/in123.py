import math 
def num_stats(x):
    if x is not int:
        raise TypeError('Work with Numbers Only')
    if x < 0:
        raise ValueError('Work with Positive Numbers Only')
    print(f'{x} square is {x * x}')
    print(f'{x} square root is {math.sqrt(x)}')

x = int(input())
num_stats(x)

