# -*- coding: utf-8 -*-
import yaml
import os
import pexpect
import getpass
import telnetlib
from pprint import pprint

'''
pexpect.spawn позволяет взаимодействовать с вызванной программой, 
отправляя данные и ожидая ответ
'''

def sh_ip_int_br(device):
    ssh = pexpect.spawn('ssh cisco@192.168.100.1')
    ssh.expect(['password', 'Password'])
    ssh.sendline('cisco')
    ssh.expect('[>#]')
    ssh.sendline('enable')
    ssh.expect('[Pp]assword')
    ssh.sendline('cisco')
    ssh.expect('[>#]')
    ssh.sendline('sh ip int br')
    ssh.expect('#')
    show_output = ssh.before.decode('utf-8')
    ssh.close()
    return show_output
    
    
def send(ip, username, password, enable, commands, prompt="#"):
    telnet = telnetlib.Telnet('192.168.100.1')
    telnet.read_until(b'Username')
    telnet.write(b'cisco\n')
    telnet.read_until(b'Password')
    telnet.write(b'sh arp\n')
    telnet.write(b'sh clock\n')
    telnet.write(b'sh ip int br\n')
    telnet.read_until(b'>')
    
    
def send_show_command(ip, username, password, enable, commands, prompt="#"):
    telnet = telnetlib.Telnet('192.168.100.1')
    print(telnet.read_until(b'Username'))
    telnet.write(b'cisco\n')
    telnet.read_until(b'Password')
    telnet.write(b'cisco\n')
    #print()
    print(telnet.read_until(b'>'))
    telnet.write(b'sh ip int br\n')
    print(telnet.read_until(b'>'))
    
    
    
    
    
def bash_ls_ls(device):
    p = pexpect.spawn('/bin/bash -c "ls -ls | grep task"')
    p.expect(pexpect.EOF)
    print(p.before.decode('utf-8'))
   
    
    
if __name__ == "__main__":
    devices = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    commands = ["sh clock", "sh int desc"]
    for ip in devices:
        result = send(ip, "cisco", "cisco", "cisco", commands)
        pprint(result, width=120)

    
    
    
    
