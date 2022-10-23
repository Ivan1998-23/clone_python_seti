#!/usr/bin/env python 
'''
  25_4
        СОРТИРОВКА
    Активные записи:
    Неактивные записи:
при запросе информации, сначала должны отображаться активные записи, а затем,
неактивные. Если неактивных записей нет, не отображать заголовок «Неактивные записи».
'''
import sqlite3
import os
import yaml
from pprint import pprint
import re
import sys
from tabulate import tabulate

name_db = 'dhcp_snooping.db'

def select_dhcp_akt_noakt(cursor, param = 'active', vul=1, akt_or_not='Активные'):
    cursor.execute('SELECT * FROM dhcp WHERE {} = "{}"'.format(param, vul)) 
    next_row = cursor.fetchall() 
    if len(next_row) >0 :
        print('\n{} записи:\n'.format(akt_or_not)) 
        print(tabulate(next_row)) 
    
    
    
def select_dhcp(cursor):
    print('В таблице dhcp такие записи: ')
    select_dhcp_akt_noakt(cursor,param = 'active', vul=1, akt_or_not='Активные') 
    select_dhcp_akt_noakt(cursor,param = 'active', vul=0, akt_or_not='Неактивные')
    
def select_dhcp_paramerts(cursor, parameters, value):
    print('Информация об устройствах с такими параметрами:',
           '{} {}'.format(parameters, value))
    cursor.execute('SELECT * FROM dhcp WHERE {} = "{}"'.format(parameters, value))
    next_row = cursor.fetchall() 
    
    list_neaktiv = []
    list_aktiv = []
    for row in next_row:
        if row[5] == 1:
            list_aktiv.append(row)
        else:
            list_neaktiv.append(row)
    if len(list_aktiv) > 0:
        print('\nАктивные записи:\n') 
        print(tabulate(list_aktiv))
    elif len(list_neaktiv) > 0:
        print('\nНеактивные записи:\n') 
        print(tabulate(list_neaktiv))
    
    
def select_data():
    arguments = sys.argv[:]  
    
    db_exist = os.path.exists(name_db)
    if db_exist == False:
        print('База данных не существует. Перед выводом данных, ее надо создать')
    else: 
        conn = sqlite3.connect(name_db) 
        cursor = conn.cursor()
        
        if len(arguments) == 1:
            select_dhcp(cursor)

        elif len(arguments) == 3:
            parameters = arguments[1] 
            value = arguments[2] 
            all_parameters = []
            bool_par = False
            
            cursor.execute("pragma table_info(dhcp);")
            next_row = cursor.fetchall()  
            for i in next_row:
                all_parameters.append(i[1])  
                if parameters in i[1]:
                    bool_par = True 
                    break
            if   bool_par == True:
                select_dhcp_paramerts(cursor, parameters, value)  
            else:
                print('Данный параметр не поддерживается.')
                print('Допустимые значения параметров:', ', '.join(all_parameters))
            
            
        else:
            print('Пожалуйста, введите два или ноль аргументов')
        
        conn.commit() 



if __name__ == '__main__':  
    select_data()








