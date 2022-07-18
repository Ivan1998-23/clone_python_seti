# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re


def get_ip_from_cfg(name_file):
    
    #regex = re.compile(r'ip address +(?P<ip>\S) +(?P<mask>\S)')
    '''
    f1 = open(name_file, 'r')
    text_f1 = f1.read()
    match = re.search(r'interface (\S+)'
                    r'\n*'
                    r' +ip address (\S+) (\S+)', text_f1)
    if match:
        print(match.groups())
    '''
    with  open(name_file, 'r') as f1:
        d = {}
        for line in f1:
            if line == '!':
                interface = None
                ip = None
                mas = None
                match = None
            match = re.search(r'^interface (\S+)$', line)
            if match:
                interface = match.groups()[0]
                
            match = re.search(r' +ip address (\S+) (\S+)', line)
            if match:
                ip = match.groups()[0]
                mas = match.groups()[1]
                d[interface] = (ip, mas)
            
    return d
    

if __name__ == '__main__':
    print(get_ip_from_cfg('config_r1.txt'))
    
    
    
    
    
    
    
    
