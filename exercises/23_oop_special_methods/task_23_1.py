# -*- coding: utf-8 -*-

"""
Задание 23.1

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также должна выполняться проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать
исключение ValueError с соответствующим текстом (вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра:
ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

"""
import ipaddress


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
        return f"IPadress: {self.ip_masc}"
    def __repr__(self):
        return f"IPAddress('{self.ip_masc}')"



if __name__ == '__main__':
    r1 = IPAddress('10.9.127.121/21')
    #ip2 = IPAddress('105.2.2.2/24')
    print(r1.mask)
    #print(ip2.ip)
    '''
    print(str(r1))
    ip_addresses = [r1, ip2]
    print(ip_addresses)
    '''
