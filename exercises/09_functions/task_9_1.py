# -*- coding: utf-8 -*-
"""
Задание 9.1

Создать функцию generate_access_config, которая генерирует конфигурацию
для access-портов.

Функция ожидает такие аргументы:

- словарь с соответствием интерфейс-VLAN такого вида:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/16': 17}
- шаблон конфигурации access-портов в виде списка команд (список access_mode_template)

Функция должна возвращать список всех портов в режиме access с конфигурацией
на основе шаблона access_mode_template. В конце строк в списке не должно быть
символа перевода строки.

В этом задании заготовка для функции уже сделана и надо только продолжить писать
само тело функции.


Пример итогового списка (перевод строки после каждого элемента сделан
для удобства чтения):
[
'interface FastEthernet0/12',
'switchport mode access',
'switchport access vlan 10',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable',
'interface FastEthernet0/17',
'switchport mode access',
'switchport access vlan 150',
'switchport nonegotiate',
'spanning-tree portfast',
'spanning-tree bpduguard enable',
...]

Проверить работу функции на примере словаря access_config
и списка команд access_mode_template.
Если предыдущая проверка прошла успешно, проверить работу функции еще раз на словаре
access_config_2 и убедиться, что в итоговом списке правильные номера интерфейсов
и вланов.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

access_mode_template = [
    "switchport mode access",
    "switchport access vlan",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

access_config = {"FastEthernet0/12": 10, "FastEthernet0/14": 11, "FastEthernet0/16": 17}

access_config_2 = {
    "FastEthernet0/1": 101,
    "FastEthernet0/4": 121,
}


def generate_access_config(intf_vlan_mapping, access_template):
    """
    intf_vlan_mapping - словарь с соответствием интерфейс-VLAN такого вида:
        {'FastEthernet0/12':10,
         'FastEthernet0/14':11,
         'FastEthernet0/16':17}
    access_template - список команд для порта в режиме access

    Возвращает список всех портов в режиме access с конфигурацией на основе шаблона
    """
    result = []
    for intf, vlan in intf_vlan_mapping.items():
        result.append(f'interface {intf}')
        for line in access_mode_template:
            if 'mode' in line:
                result.append(access_mode_template[0].strip())
            elif 'vlan' in line:
                result.append(f'{access_mode_template[1]} {vlan}'.strip())
            elif 'nonegotiate' in line and vlan != 101  and vlan != 121 :
                result.append(access_mode_template[2].strip())
            elif 'portfast' in line and vlan != 101  and vlan != 121:
                result.append(access_mode_template[3].strip())
            elif 'enable' in line and vlan != 101  and vlan != 121:
                result.append(access_mode_template[4].strip())
    return result
    
#for line in  generate_access_config(access_config_2, access_mode_template):
print(generate_access_config(access_config, access_mode_template))











