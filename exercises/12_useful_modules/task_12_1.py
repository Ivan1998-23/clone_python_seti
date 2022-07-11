# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.


if __name__ == '__main__':
    print(ping_i)
    
    
"""
import subprocess



list_of_ips = ["1.1.1.1", "8.8.8.8", "8.8.4.4", "8.8.7.1"]




def ping_ip_addresses(list_ip):
    list_ok = []
    list_er = []
    for ip in list_ip:
        reply = subprocess.run(['ping', '-c', '1', '-n',  ip])
        if reply.returncode == 0:
            list_ok.append(ip)
        elif reply.returncode == 1:
            list_er.append(ip)
    result = (list_ok, list_er)
    return result


if __name__ == '__main__':
    print(ping_ip_addresses(list_of_ips))
    
    


