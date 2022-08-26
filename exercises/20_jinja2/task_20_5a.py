# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
from task_20_1 import generate_config
import yaml
from netmiko import (ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException)
import netmiko
import re
import pexpect
from pprint import pprint
data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}
data2 = {
        "tun_num": None,
        "wan_ip_1": "80.241.1.1",
        "wan_ip_2": "90.18.10.2",
        "tun_ip_1": "10.255.1.1 255.255.255.252",
        "tun_ip_2": "10.255.1.2 255.255.255.252",
    }
src_template = 'templates/gre_ipsec_vpn_1.txt'
dst_template = 'templates/gre_ipsec_vpn_2.txt'


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    
    tunel_src = set_tunnel(src_device_params)
    tunel_dst = set_tunnel(dst_device_params)
    
    l = True
    iterator = 0
    while l:
        if (iterator  not in tunel_src) and (iterator  not in tunel_dst):
            l = False
        else:
            iterator += 1
    vpn_data_dict["tun_num"] = iterator
    
    output_list_1 = conf_src = generate_config(src_template, vpn_data_dict)
    output_list_2 = conf_dst = generate_config(dst_template, vpn_data_dict)
    
    send_config_set(src_device_params, conf_src.split('\n'))
    send_config_set(dst_device_params, conf_dst.split('\n'))
    c = ['crypto isakmp policy 10', 'encr aes', 'authentication pre-share', 'group 5', 'hash sha', 'crypto isakmp key cisco address 192.168.100.2', 'crypto ipsec transform-set AESSHA esp-aes esp-sha-hmac', 'mode transport', 'crypto ipsec profile GRE', 'set transform-set AESSHA', 'interface Tunnel 10', 'ip address 10.0.1.1 255.255.255.252', 'tunnel source 192.168.100.1', 'tunnel destination 192.168.100.2', 'tunnel protection ipsec profile GRE']
       

    return (output_list_1, output_list_2)



def send_config_set(device, conf_com):
    try:
        with ConnectHandler(**device) as ssh:
            
            ssh.enable()
            ssh.config_mode()
            result = ssh.send_config_set(conf_com)
            return result 
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as r:
        print(r)



        
'''        
# Подключаемся по SSH  чтобы убрать --More--
def set_tunnel(device, prompt="#"):
    with pexpect.spawn(f"ssh {device.get('username')}@{device.get('host')}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(device.get('password'))
        enable_status = ssh.expect([">", "#"])
        if enable_status == 0:
            ssh.sendline("enable")
            ssh.expect("[Pp]assword")
            ssh.sendline(device.get('secret'))
            ssh.expect(prompt)
        
        ssh.sendline('sh ip int')
        output = ""
        
        while True:
            match = ssh.expect([prompt, "--More--", pexpect.TIMEOUT])
            page = ssh.before.replace("\r\n", "\n")
            page = re.sub(" +\x08+ +\x08+", "\n", page)
            output += page
            if match == 0:
                break
            elif match == 1:
                ssh.send(" ")
            else:
                print("Ошибка: timeout")
                
                break
        output = re.sub("\n +\n", "\n", output)
            
        
        res = re.finditer(r'.*Tunnel(\S*).*', output)
        groups =[]
        for match in res:
            groups.append(int(match.groups()[0]))
        
        return groups 
        
'''
def set_tunnel(device):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command('sh ip int br')
            #print(result)
        res = re.finditer(r'.*Tunnel(\S*).*', result)
        groups =[]
        for match in res:
            groups.append(int(match.groups()[0]))
        
        return groups 
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as r:
        print(r)


if __name__ == '__main__':
    dev = 'devices.yaml'
    with open(dev) as f1:
        tem = yaml.safe_load(f1)
    src_device_params = tem[0]
    dst_device_params = tem[1]
    print(configure_vpn(src_device_params, dst_device_params, src_template, dst_template, data))
    
    
