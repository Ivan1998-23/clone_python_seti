# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
vlans = int(input())
b= []
with open('CAM_table.txt', 'r') as f1:
    for lin in f1:
        if '/' in lin:
            a = lin.split()
            a[0] = int(a[0])
            a.remove(a[2])
            b.append(a)
        
b.sort()

for i in b:
    if i[0] == vlans:
        print("{:<9}{:20}{:15}".format(i[0], i[1], i[2]))


