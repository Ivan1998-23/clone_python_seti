# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


def get_int_vlan_map(config_filename):
    cl_as = {}
    cl_tr = {}
    intf = None
    
    with open(config_filname, 'r') as f1:        
        for line in f1:
            vl = []
            vlan = None
            vlans = None
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
            elif 'duplex' in line and cl_as.get(intf) == None and cl_tr.get(intf) == None :
                print(cl_as.get(intf) )
                cl_as[intf] = 1
    tpl = (cl_as, cl_tr)
    return tpl
                                       
config_filname = 'config_sw2.txt'

print(get_int_vlan_map(config_filname))
