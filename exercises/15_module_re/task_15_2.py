# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция долж
на обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface 
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""
import re

def parse_sh_ip_int_br(name_file):
    with open(name_file, 'r') as f1:
        mas = []
        for line in f1:
            match = re.search(r"(\S+)\s+(\S+)\s+YES\s+\S+\s+(\S*)\s+(\S+)\n", line)  
            if match:
                mas.append(match.groups())
            else:
                match = re.search(r"(\S+)\s+(\S+)\s+YES\s+\S+\s+(\S*\s+down)\s+(\S+)", line)
                if match:
                    mas.append(match.groups())
    return mas

headers = ["hostname", "ios", "platform"]
data = [("R1", "12.4(24)T1", "Cisco 3825"), ("R2", "15.2(2)T1", "Cisco 2911"), ("SW1", "12.2(55)SE9", "Cisco WS-C2960-8TC-L")]

def convert_to_dict(headers, data):
        ms = []
        
        for i in range(len(data)):
            k = {}
            for j in range(len(headers)):
                k[headers[j]] = data[i][j]
                print(k)
            ms.append(k)
        print(ms)



if __name__ == '__main__':
    name_file = 'sh_ip_int_br.txt' #input()
    print(parse_sh_ip_int_br(name_file))
    #convert_to_dict(headers, data)
    
    





















