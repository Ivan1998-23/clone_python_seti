# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""
import yaml
from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)


# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands =  correct_commands + commands_with_errors
#commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]

def send_config_commands(device, config_commands, log = True):
    result_ok = {}
    result_on = {}
    dict_all = ()
    out_com = []
    try:
        with ConnectHandler(**device) as ssh:
            if log:
                print('Подключаюсь к', device.get('host')+'...')
                
            ssh.enable()
            conf = ssh.config_mode()
            for com in config_commands:                
                com_in = ssh.send_command(com)
                if 'Invalid input detected' in com_in: #result.get(com):
                    result_on[com] = conf + com + com_in + '\n' + ssh.find_prompt()
                    print('Команда {} выполнилась с ошибкой'.format(com),
                    '"Invalid input detected." на устройстве {}'.format(device.get('host')))
                    yes_or_not = str(input('Продолжать выполнять команды? [y]/n: '))
                    if yes_or_not == 'n' or yes_or_not == 'no':
                        break
                    else:
                        continue
                elif 'Incomplete command' in com_in: #result.get(com):
                    result_on[com] = conf+ com + com_in + '\n' + ssh.find_prompt()
                    print('Команда {} выполнилась с ошибкой'.format(com),
                    '"Incomplete command." на устройстве {}'.format(device.get('host')))
                    yes_or_not = str(input('Продолжать выполнять команды? [y]/n: '))
                    if yes_or_not == 'n' or yes_or_not == 'no':
                        break
                    else:
                        continue
                elif 'Ambiguous command' in com_in: #result.get(com):
                    result_on[com] = conf+ com + com_in + '\n' + ssh.find_prompt()
                    print('Команда {} выполнилась с ошибкой'.format(com),
                    '"Ambiguous command." на устройстве {}'.format(device.get('host')))
                    yes_or_not = str(input('Продолжать выполнять команды? [y]/n: '))
                    if yes_or_not == 'n' or yes_or_not == 'no':
                        break
                    else:
                        continue
                else:
                    result_ok[com] = conf+ com + '\n' + com_in + '\n' + ssh.find_prompt()
        return (result_ok, result_on)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == '__main__':
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    
    for dev in devices:
        ok, on = send_config_commands(dev, commands)
    print(ok.keys())
    print(on.keys())
