# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re


name_file = 'sh_cdp_n_sw1.txt'

def parse_sh_cdp_neighbors(list_file):
    
    name_r = re.search(r'(\S+)[#>].+', list_file)
    if name_r:
        name_r = name_r.groups()[0]
    
    regex = r'(\S+)\s+(\S+\s+\d+/\d+)\s+\S+\s+.+\S+\s+\S+\s+(\S+\s+\d+/\d+)\n'    
    result = re.finditer(regex, list_file)
    
    groups =[]
    for match in result:
        groups.append(match.groups())
        
    dict_r = {name_r: {}}
    #print(dict_r)
    
    for i in range(len(groups)):
        #print(groups[i])
        f_r = {groups[i][1]: {groups[i][0] : groups[i][2]}}
        dict_r[name_r].update(f_r)
    
    
    
    return dict_r




if __name__ == '__main__':
    
    with open(name_file, 'r') as f1:
        print(parse_sh_cdp_neighbors(f1.read()))









