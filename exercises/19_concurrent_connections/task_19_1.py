# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import yaml
import subprocess
from concurrent.futures import ThreadPoolExecutor


ip_list = ['192.168.100.1', '192.168.1.1', '192.168.100.2', '192.168.100.3','192.168.100.4']
limit = 2

def ping_ip_addresses(ip_list, limit=3):
    list_ok_ip = []
    list_on_ip = []
    
    with ThreadPoolExecutor(max_workers = limit) as executor:
        result = executor.map(ping_one_host, ip_list)
        
    for ip, log in result:
        if log:
            list_ok_ip.append(ip)
        else:
            list_on_ip.append(ip)
    return (list_ok_ip, list_on_ip)

def ping_one_host(ip):
    reply = subprocess.run(['ping', '-c', '1', '-n', ip], stdout = subprocess.PIPE)
    if reply.returncode == 0:
        return ip, True
    else:
        return ip, False


if __name__ == '__main__':
    print(ping_ip_addresses(ip_list))
        









