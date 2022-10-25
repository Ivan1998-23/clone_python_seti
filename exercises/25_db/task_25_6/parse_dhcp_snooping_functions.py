#!/usr/bin/env python 
from create_db import create_db as cr_db
from add_data import insert_data 
from get_data import select_dhcp_paramerts
from get_data import select_data


namedb = 'dhcp_snooping.db'
namesql = 'dhcp_snooping_schema.sql'

switch_inf = 'switches.yml'
sw1_inf = 'sw1_dhcp_snooping.txt'
sw2_inf = 'sw2_dhcp_snooping.txt'
sw3_inf = 'sw3_dhcp_snooping.txt' 
sw_all = [sw1_inf, sw2_inf, sw3_inf]
key = 'ip'
value = '192.168.100.100'


def create_db(name, schema): 
    cr_db(name, schema)

def add_data_switches(db_file, switch_inf):
    insert_data(db_file,  switch_inf, 'switches')

def add_data(db_file, filename):
    insert_data(db_file,  filename, 'dhcp')

def get_all_data(db_file):
    select_data(db_file)

def get_data(db_file, key, value):
    select_dhcp_paramerts(db_file, key, value)



if __name__ == '__main__':
    #create_db(namedb, namesql)
    
    #add_data_switches(namedb, switch_inf)
    #add_data(namedb, sw_all)
    get_data(namedb, key, value)
    #get_all_data(namedb)
