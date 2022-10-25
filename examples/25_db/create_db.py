#!/usr/bin/env python
''' create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
- должна выполняться проверка наличия файла БД    
- если файла нет, согласно описанию схемы БД в файле 
    dhcp_snooping_schema.sql, должна быть создана БД
- имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
• switches - в ней находятся данные о коммутаторах
• dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding
'''
import sqlite3
import os




name_db = 'dhcp_snooping.db'
name_sql = 'dhcp_snooping_schema.sql'

#Получение списка файлов в директории
def show_filies(name_db = None):
    path = os.getcwd()
    print('-'*40)
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            # печать всех записей, являющихся файлами
            if entry.is_file():
                if name_db == None:
                    print(' -',entry.name)
                elif name_db in entry.name:
                    print(' #',entry.name)
                else:
                    print(' -',entry.name)
    print('-'*40)

def create_db():
    #проверка есть ли БД 
    db_exist = os.path.exists(name_db)
    
    if db_exist:
        print('База данных существует')
        delet_db = input('Удалить БД (y/n) ? ')
        if delet_db in "yes":  
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name_db)
            os.remove(path)  
            show_filies() 
        else:  
            show_filies(name_db) 
    else:
        print('Создаю базу данных...')
        conn = sqlite3.connect(name_db) 
        with open(name_sql, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
        conn.close()


if __name__ == '__main__':
    create_db()
