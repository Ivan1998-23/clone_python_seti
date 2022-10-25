#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
$ python parse_dhcp_snooping.py get -h 
$ python parse_dhcp_snooping.py add -h    
$ python parse_dhcp_snooping.py create_db
        Создаю БД dhcp_snooping.db со схемой dhcp_snooping_schema.sql
        Создаю базу данных... 
$ python parse_dhcp_snooping.py add sw[1-3]_dhcp_snooping.txt
        Читаю информацию из файлов
        sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
        Добавляю данные по DHCP записях в dhcp_snooping.db
$ python parse_dhcp_snooping.py add -s switches.yml
        Добавляю данные о коммутаторах
$ python parse_dhcp_snooping.py get
        В таблице dhcp такие записи:
        Активные записи:
        -----------------  ---------------  --  ----------------  ---  -  -------------------
        00:09:BB:3D:D6:58  10.1.10.2        10  FastEthernet0/1   sw1  1  2019-03-08 16:47:52
        00:04:A3:3E:5B:69  10.1.5.2          5  FastEthernet0/10  sw1  1  2019-03-08 16:47:52
        00:05:B3:7E:9B:60  10.1.5.4          5  FastEthernet0/9   sw1  1  2019-03-08 16:47:52
        00:07:BC:3F:A6:50  10.1.10.6        10  FastEthernet0/3   sw1  1  2019-03-08 16:47:52
        00:09:BC:3F:A6:50  192.168.100.100   1  FastEthernet0/7   sw1  1  2019-03-08 16:47:52
        00:A9:BB:3D:D6:58  10.1.10.20       10  FastEthernet0/7   sw2  1  2019-03-08 16:47:52
        00:B4:A3:3E:5B:69  10.1.5.20         5  FastEthernet0/5   sw2  1  2019-03-08 16:47:52
        00:C5:B3:7E:9B:60  10.1.5.40         5  FastEthernet0/9   sw2  1  2019-03-08 16:47:52
        00:A9:BC:3F:A6:50  10.1.10.60       20  FastEthernet0/2   sw2  1  2019-03-08 16:47:52
        00:E9:BC:3F:A6:50  100.1.1.6         3  FastEthernet0/20  sw3  1  2019-03-08 16:47:52
        -----------------  ---------------  --  ----------------  ---  -  -------------------
$ python parse_dhcp_snooping.py get -k vlan -v 10
        Данные из БД: dhcp_snooping.db
        Информация об устройствах с такими параметрами: vlan 10
        Активные записи:
        -----------------  ----------  --  ---------------  ---  -  -------------------
        00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1  2019-03-08 16:47:52
        00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/3  sw1  1  2019-03-08 16:47:52
        00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1  2019-03-08 16:47:52
        -----------------  ----------  --  ---------------  ---  -  -------------------
$ python parse_dhcp_snooping.py get -k vln -v 10
        usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                          [-k {mac,ip,vlan,interface,switch}]
                                          [-v VALUE] [-a]
        parse_dhcp_snooping.py get: error: argument -k: invalid choice: 'vln' (choose from 'mac', 'ip', 'vlan', 'interface', 'switch')
'''
import argparse

import parse_dhcp_snooping_functions as pds

# Default values:
DFLT_DB_NAME = "dhcp_snooping.db"
DFLT_DB_SCHEMA = "dhcp_snooping_schema.sql"


def create(args):
    print("Создаю БД {} со схемой {}".format(args.name, args.schema))
    pds.create_db(args.name, args.schema)


def add(args):
    if args.sw_true:
        print("Добавляю данные о коммутаторах")
        pds.add_data_switches(args.db_file, args.filename)
    else:
        print("Читаю информацию из файлов\n{}".format(", ".join(args.filename)))
        print("\nДобавляю данные по DHCP записям в {}".format(args.db_file))
        pds.add_data(args.db_file, args.filename)


def get(args):
    if args.key and args.value:
        print("Данные из БД: {}".format(args.db_file))
        print("Информация об устройствах с такими параметрами:", args.key, args.value)
        pds.get_data(args.db_file, args.key, args.value)
    elif args.key or args.value:
        print("Пожалуйста, введите два или ноль аргументов\n")
        print(show_subparser_help("get"))
    else:
        print("В таблице dhcp такие записи:")
        pds.get_all_data(args.db_file)


def show_subparser_help(subparser_name):
    """
    Function returns help message for subparser
    """
    subparsers_actions = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    return subparsers_actions[0].choices[subparser_name].format_help()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    title="subcommands", description="команды", help="дополнительная информация"
)

create_parser = subparsers.add_parser("create_db", help="создать новую базу данных")
create_parser.add_argument("-n", dest="name", default=DFLT_DB_NAME, help="имя БД")
create_parser.add_argument("-s", dest="schema", default=DFLT_DB_SCHEMA, help="схема БД")
create_parser.set_defaults(func=create)

add_parser = subparsers.add_parser("add", help="добавить данные в БД")
add_parser.add_argument("filename", nargs="+", help="файл(ы), которые надо добавить")
add_parser.add_argument("--db", dest="db_file", default=DFLT_DB_NAME, help="имя БД")
add_parser.add_argument(
    "-s",
    dest="sw_true",
    action="store_true",
    help=(
        "если флаг установлен, добавлять "
        "данные коммутаторов, иначе добавлять DHCP записи"
    ),
)
add_parser.set_defaults(func=add)

get_parser = subparsers.add_parser("get", help="отобразить данные из БД")
get_parser.add_argument("--db", dest="db_file", default=DFLT_DB_NAME, help="имя БД")
get_parser.add_argument(
    "-k",
    dest="key",
    choices=["mac", "ip", "vlan", "interface", "switch"],
    help="параметр для поиска записей",
)
get_parser.add_argument("-v", dest="value", help="значение параметра")
get_parser.add_argument("-a", action="store_true", help="показать все содержимое БД")
get_parser.set_defaults(func=get)

if __name__ == "__main__":
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)
