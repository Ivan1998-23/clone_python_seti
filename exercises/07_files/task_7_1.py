# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
result = {}
with open("ospf.txt", 'r') as f:
    for line in f:
        print()
        print('{:22}{:5}'.format('Prefix', line.split()[1]))        
        print('{:22}{:5}'.format('AD/Metric', line.split()[2].strip("[]")))
        print('{:22}{:5}'.format('Next-Hop', line.split()[4].strip(',')))
        print('{:22}{:5}'.format('Last update', line.split()[5].strip(',')))
        print('{:22}{:5}'.format('Outbound Interface', line.split()[-1]))
        print()
