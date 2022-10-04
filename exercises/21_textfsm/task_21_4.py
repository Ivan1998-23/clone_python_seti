# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
import yaml
import netmiko
from textfsm import clitable


def  send_and_parse_show_command(device_dict, command, templates_path, index = 'index'):
    
    ssh = netmiko.ConnectHandler(**device_dict)
    ssh.enable()
    result = ssh.send_command(command)
    
    cli_table = clitable.CliTable(index, templates_path)
    atributes = {'Command' : command}
    cli_table.ParseCmd(result, atributes)
    
    data_rows = [list(row) for row in cli_table]
    
    header = list(cli_table.header)
    
    result = []
    
    for cil_list in data_rows:
        end_dict = {}
    
        for i in range(len(cil_list)):
            end_dict[str(header[i])] = cil_list[i]
        result.append(end_dict)
        
    return result
    


if __name__ == '__main__':
    command = 'sh ip int br'
    templates_path = 'templates'
    
    with open('devices.yaml') as f1:
        templates = yaml.safe_load(f1)
    
    print(send_and_parse_show_command(templates[0], command, templates_path))
