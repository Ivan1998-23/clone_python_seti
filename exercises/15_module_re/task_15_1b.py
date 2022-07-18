# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них.

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re


def get_ip_from_cfg(name_file):
    with  open(name_file, 'r') as f1:
        d = {}
        ip = None
        for line in f1:
            if line == '!\n':
                interface = None
                ip = None
                mas = None
                match = None
            match = re.search(r'^interface (\S+)$', line)
            if match:
                interface = match.groups()[0]
                
            match = re.search(r' +ip address (\S+) (\S+)', line)
            if match:
                if ip == None:
                    ip = match.groups()[0]
                    mas = match.groups()[1]
                    d[interface] = [(ip, mas)]
                else:
                    ip_1 = match.groups()[0]
                    mas_1 = match.groups()[1]
                    d[interface] = [(ip, mas), (ip_1, mas_1)]
    return d
    

if __name__ == '__main__':
    print(get_ip_from_cfg('config_r2.txt'))



