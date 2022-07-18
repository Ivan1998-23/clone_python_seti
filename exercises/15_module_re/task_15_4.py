# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re

def get_ints_without_description(name_file_config):
    list_name = []
    with open(name_file_config, 'r') as f1:
        dict_int = []
        interface = None
        for line in f1:
            if ('!' in line) and (interface != None):
                dict_int.append(interface)
                interface = None
            else:
                match = re.search(r'^interface\s+(?P<int>\S+)', line)
                if match:
                    interface = match.groups()[0]
                elif 'description' in line:
                    interface = None
    return dict_int
    
    
    
    
if __name__ == '__main__':
    n_f = input()
    print(get_ints_without_description('config_r1.txt'))







