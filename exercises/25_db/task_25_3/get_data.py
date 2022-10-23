#!/usr/bin/env python 
import sqlite3
import os
import yaml
from pprint import pprint
import re
import sys
from tabulate import tabulate

name_db = 'dhcp_snooping.db'

def select_dhcp(cursor):
    cursor.execute('SELECT * FROM dhcp') 
    next_row = cursor.fetchall() 
    print('В таблице dhcp такие записи:')
    print(tabulate(next_row)) 
    
def select_dhcp_paramerts(cursor, parameters, value):
    cursor.execute('SELECT * FROM dhcp WHERE {} = "{}"'.format(parameters, value))
    next_row = cursor.fetchall() 
    print('Информация об устройствах с такими параметрами: {} {}'.format(parameters, value))
    print(tabulate(next_row)) 
    
    
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
