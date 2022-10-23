#!/usr/bin/env python  
'''
      ADD pararmetrs ACTIVET

выполнялись новые условия и заполня-
лось поле active.
Код в скрипте должен быть разбит на функции. Какие именно функции и как разделить код,
надо решить самостоятельно. Часть кода может быть глобальной.
'''

import sqlite3
import os
import yaml
from pprint import pprint
import re
name_db = 'dhcp_snooping.db'
switch_inf = 'switches.yml'
sw1_inf = 'new_data/sw1_dhcp_snooping.txt'
sw2_inf = 'new_data/sw2_dhcp_snooping.txt'
sw3_inf = 'new_data/sw3_dhcp_snooping.txt'

sw_all = [sw1_inf, sw2_inf, sw3_inf]

def insert_db(cursor, data, query):
    #Запись иформации в БД 
    for row in data:
        try:
            cursor.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('При добавлении данных: {} Возникла ошибка: {}'.format(row, e))
    

def insert_sw(cursor):
    print('Добавляю данные в таблицу switches...')
    
    #считываю инфу с файла УМЛ
    with open(switch_inf, 'r') as f1:
        templetes = yaml.safe_load(f1) 
    
    #Переабразую словарь в список кортежей
    data = []
    query = "INSERT into switches values (?, ?)" 
    for i, v in templetes.get('switches').items(): 
        data.append((i, v))
        
    insert_db(cursor, data, query)     
    
    
def insert_dhcp(cursor): 
    print('Добавляю данные в таблицу dhcp...')
    query = "REPLACE INTO dhcp values (?, ?, ?, ?, ?, ?)" 
    cursor.execute('UPDATE dhcp set active = "0"')
    for sw in sw_all:
        with open(sw, 'r') as f1:
            out = f1.read()
        regex = r'(\S*) *(\d*\.\d*\.\d*\.\d*) *\d* *\S* *(\d*) *(\S*)'
        switch_name = sw.split('_')[0]
        data = [match.groups() + (switch_name, 1)   for match in re.finditer(regex, out)]
     
        insert_db(cursor, data, query)
    
    
    
def insert_data():
    db_exist = os.path.exists(name_db)
    if db_exist == False:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    else: 
        conn = sqlite3.connect(name_db) 
        cursor = conn.cursor()
        
        #insert_sw(cursor)
        insert_dhcp(cursor)  
        conn.commit()
        
        
        
if __name__ == '__main__':  
    insert_data()
