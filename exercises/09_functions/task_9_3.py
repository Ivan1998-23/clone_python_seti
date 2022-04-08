# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""



def get_int_vlan_map(config_filename):
    cl_as = {}
    cl_tr = {}
    intf = None
    
    with open(config_filname, 'r') as f1:        
        for line in f1:
            vl = []
            if 'interface' in line  and '/' in line :
                intf = line.split()[1]                
            elif 'vlan' in line and 'access' in line: 
                vlan = int(line.split()[3])
                cl_as[intf] = vlan
            elif 'vlan' in line and 'trunk' in line:
                
                vlans = line.split()[4].split(',')
                ii = 0
                for i in vlans:
                    vlans[ii] = int(i)
                    ii = ii + 1
                    
                cl_tr[intf] = vlans
    tpl = (cl_as, cl_tr)
    return tpl
                                       
config_filname = 'config_sw1.txt'

print(get_int_vlan_map(config_filname))

