# -*- coding: utf-8 -*-
import sys
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]


f_input = sys.argv[1]
f_output = sys.argv[2]

with open(f_input, 'r') as f1, open(f_output, 'w') as f2:
    for line in f1:
        if '!' in line:
            pass
        else:
            log = False
            for q in ignore:                
                if q in line:
                    log = True
            if log == False:
                f2.write(line)


