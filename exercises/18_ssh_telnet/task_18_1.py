# -*- coding: utf-8 -*-
"""
Задание 18.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству
и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml
с помощью функции send_show_command (эта часть кода написана).

"""
import yaml
import os
import pexpect
import getpass
import netmiko
from pprint import pprint
from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)
'''
pexpect.spawn позволяет взаимодействовать с вызванной программой, 
отправляя данные и ожидая ответ
'''
def sh_ip_int_br(device):
    ssh = pexpect.spawn('ssh cisco@192.168.100.1')
    ssh.expect(['password', 'Password'])
    ssh.sendline('cisco')
    ssh.expect('[>#]')
    ssh.sendline('enable')
    ssh.expect('[Pp]assword')
    ssh.sendline('cisco')
    ssh.expect('[>#]')
    ssh.sendline('sh ip int br')
    ssh.expect('#')
    show_output = ssh.before.decode('utf-8')
    ssh.close()
    return show_output


def bash_ls_ls(device):
    p = pexpect.spawn('/bin/bash -c "ls -ls | grep task"')
    p.expect(pexpect.EOF)
    print(p.before.decode('utf-8'))

def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        return result
    
if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    
    for dev in devices:
        print(send_show_command(dev, command))
        
        
        
        
    '''
    print(bash_ls_ls(devices[1]))
    
    #print(sh_ip_int_br(devices[1]))
    '''




