# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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

topology_example2 = {
    ("R33", "Eth0/4"): ("R7", "Eth0/0"),
    ("R22", "Eth0/6"): ("R9", "Eth0/0"),
}




class Topology:  
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        
    
    def _normalize(self, topology_dict):
        result = {}
        for key, val  in topology_dict.items():
            if  key != result.get(val, False):
                result[key] = val 
        return result 
    
    def delete_link(self, keys, value):
        if value == self.topology.get(keys, False):
            self.topology.pop(keys)
        elif keys == self.topology.get(value, False):
            self.topology.pop(value)
        else:
            print('Такого соединения нет')
        
    def __add__ (self, other): 
        result = {}
        result.update(self.topology)
        result.update(other.topology)
        return Topology(result)
    
    def __str__(self):
        return self.topology
    
    def __repr__(self):
        return f"IPAddress('{self.topology}')"
        
    def __iter__(self):
        result = []
        for i, j in self.topology.items(): 
            result.append((i,j)) 
        return iter(result)
        
if __name__ == "__main__":
    top = Topology(topology_example)
    for i in top:
        print(i)
