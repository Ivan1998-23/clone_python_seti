#import task_4_1 
from task_4_1 import nat

a = nat.split()
a[7] = 'GigabitEthernet0/1'
stdout = '{} {} {} {} {} {} {} {} {}'.format(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8])
print(stdout)  
