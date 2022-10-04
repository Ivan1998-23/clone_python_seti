# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""

class IPAddress:
    def __init__ (self, ip_masc):
        ip, masc = ip_masc.split('/')
        log = False
        for i in  ip.split('.'):
            if int(i) > 0 and int(i) <256:
                log = True
            else:
                raise ValueError(f" Incorrect IPv4 address")
        if int(masc) >8 and int(masc) < 32:
            pass
        else:
            raise ValueError(f" Incorrect  mask")
        
        self.ip = ip
        self.mask = int(masc)   

    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"
    def __repr__(self):
        all_ip_mac = self.ip +'/' + str(self.mask)
        return f"IPAddress('{all_ip_mac}')"



if __name__ == '__main__':
    r1 = IPAddress('10.9.127.121/21')
    print(r1.mask)
    print(r1)
    ip_list = []
    ip_list.append(r1)
    print(ip_list)
