#!/usr/bin/env python  
'''
    25_5a
        delete 7 days 
    25_5
        ADD TIME
    25_4
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
import datetime
from datetime import timedelta, datetime
from tabulate import tabulate

namedb = 'dhcp_snooping.db'
switchinf = 'switches.yml'
sw1_inf = 'sw1_dhcp_snooping.txt'
sw2_inf = 'sw2_dhcp_snooping.txt'
sw3_inf = 'sw3_dhcp_snooping.txt'

sw_all = [sw1_inf, sw2_inf, sw3_inf]

def insert_db(cursor, data, query):
    #Запись иформации в БД 
    for row in data:
        try: 
            cursor.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('При добавлении данных: {} Возникла ошибка: {}'.format(row, e))
    

def insert_sw(cursor, switch_inf):
    print('Добавляю данные в таблицу switches...')
    
    #считываю инфу с файла УМЛ
    with open(switch_inf[0], 'r') as f1:
        templetes = yaml.safe_load(f1) 
    
    #Переабразую словарь в список кортежей
    data = []
    query = "INSERT into switches values (?, ?)" 
    for i, v in templetes.get('switches').items(): 
        data.append((i, v))
        
    insert_db(cursor, data, query)     
    

def delet_7_after_date(cursor):
    cursor.execute('SELECT * FROM dhcp;') 
    next_row = cursor.fetchall()    
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    for row in next_row:
        if str(row[6]) <  str(week_ago):
            cursor.execute('DELETE  FROM dhcp WHERE last_active = "{}";'.format(row[6])) 
         



def insert_dhcp(cursor, sw_all): 
    print('Добавляю данные в таблицу dhcp...') 
    query = "REPLACE INTO dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))" 
    cursor.execute('UPDATE dhcp set active = "0"')
    for sw in sw_all:
        r =  '' + sw 
        #r =  '' + sw 
        with open(r, 'r') as f1:
            out = f1.read()
        regex = r'(\S*) *(\d*\.\d*\.\d*\.\d*) *\d* *\S* *(\d*) *(\S*)'
        switch_name = sw.split('_')[0]
        data = [match.groups() + (switch_name, 1)   for match in re.finditer(regex, out)] 
        insert_db(cursor, data, query)
        
    delet_7_after_date(cursor)
    
    
    
    
def insert_data(name_db, finame_dhcp_sw, what_tabl = None):
    db_exist = os.path.exists(name_db)
    if db_exist == False:
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    else: 
        conn = sqlite3.connect(name_db) 
        cursor = conn.cursor()
        
        if what_tabl == None: 
            insert_sw(cursor, finame_dhcp_sw)
            insert_dhcp(cursor, finame_dhcp_sw)  
        elif what_tabl == 'dhcp':
            insert_dhcp(cursor, finame_dhcp_sw) 
        elif what_tabl == 'switches':
            insert_sw(cursor, finame_dhcp_sw)
        
        conn.commit()
        
        
        
if __name__ == '__main__':   
    insert_data(namedb,  switchinf, 'switches')
    insert_data(namedb,  sw_all, 'dhcp')
    
    '''
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    print(now)
    print(week_ago)
    print(now > week_ago)
    print(str(now) > str(week_ago))
    '''





