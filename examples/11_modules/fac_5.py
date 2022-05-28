print('start')
aa = 0
bb = 0
cc = 0
dd = 0
ee = 0

for a in range(1,33):
    for b in range(1,33):
        for c in range(1,33):
            for d in range(1,33):
                if a != b and a != c and a != d and b != c and b != d and c != d:
                    if pow(a,3) + pow(b,3) == pow(c,3) + pow(d,3):
                        aa =a
                        bb = b
                        cc = c
                        dd = d
                        print(pow(a,3) + pow(b,3))
else:
    print('finich')
    print(aa,bb,cc,dd)

'''
n = int(input())
summ = 0
nub = 0
while n > 0:
    summ += n % 10
    n //= 10    
    if n == 0 and summ > 9:
        n = summ
        summ = 0
        
print(summ)
'''


