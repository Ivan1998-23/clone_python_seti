# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
c = True
while c == True:
    try:
        a = input()
        b1 = int(a.split('.')[0])
        b2 = int(a.split('.')[1])
        b3 = int(a.split('.')[2])
        b4 = int(a.split('.')[3])
        
        if b1 >= 0 and b1 <256 and b2 >= 0 and b2 <256 and b3 >= 0 and b3 <256 and b4 >= 0 and b4 <256 and (len(a.split('.')) == 4):
            if a == '0.0.0.0':
                print('unassigned')
            elif a == '255.255.255.255':
                print('local broadcast')
            elif b1 > 0 and b1 < 224:
                print('unicast')
            elif b1 > 223 and b1 < 240:
                print('multicast')
            else:
                print('unused')
        else:
            print('неправильный ip-адрес')
            continue
        c = False
    except (ValueError, IndexError, TypeError):
        print('неправильный ip-адрес')
        #continue
