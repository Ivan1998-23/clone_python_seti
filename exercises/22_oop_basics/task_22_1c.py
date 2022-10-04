# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

"""
from pprint import pprint

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    result = {}
    delet_dict_device = []
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        
    
    def _normalize(self, topology_dict):
        for key, val  in topology_dict.items():
            if  key != type(self).result.get(val, False):
                type(self).result[key] = val
                
        return self.result
    
    
    def delete_link(self, keys, value):
        if value == self.topology.get(keys, False):
            self.topology.pop(keys)
        elif keys == self.topology.get(value, False):
            self.topology.pop(value)
        else:
            print('Такого соединения нет')
    
    
    def delete_node(self, device):
        for dev, val in self.topology.items():
            if device == dev[0] or device == val[0]:
                type(self).delet_dict_device.append(dev)
                
        if len(type(self).delet_dict_device) != 0 :
            for i in type(self).delet_dict_device:
                self.topology.pop(i)
                print(i)
        else:
            print('Такого устройства нет')


if __name__ == "__main__":
    top = Topology(topology_example)
    top.delete_node("SW1")
    pprint(top.topology)
