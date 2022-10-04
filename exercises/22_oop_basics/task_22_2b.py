# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
from textfsm import clitable
import telnetlib

class CiscoTelnet:
    def __init__ (self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret        
        
        self.telnet = telnetlib.Telnet(self.ip)
        self.telnet.read_until(b'Username')
        self._write_line(self.username)
        self.telnet.read_until(b'Password')
        self._write_line(self.password)
        index, m, output = self.telnet.expect([b">", b"#"])
        if index == 0:
            self._write_line("enable")
            self.telnet.read_until(b"Password")
            self._write_line(self.secret)
            self.telnet.read_until(b"#", timeout=5)

    def _write_line(self, line):
        self.telnet.write(line.encode("ascii") + b"\n")
        
    def send_show_command(self, line, parse = True, templates = 'templates',
         index = 'index'):
        self._write_line(line)
        output_sh = self.telnet.read_until(b"#", timeout=5).decode('utf-8')
        
        if parse:
            list_shows =[]
            cli_table = clitable.CliTable(index, templates)
            atributes = {'Command' : line}
            cli_table.ParseCmd(output_sh, atributes)
            data_rows = [list(row) for row in   cli_table]
            header = list(cli_table.header)
            for i in data_rows:
                dict_sh = {} 
                for count, j in enumerate(header):
                    dict_sh[str(j)] = str(i[count])
                list_shows.append(dict_sh)
            return list_shows
        else:
            return output_sh
            
    def send_config_commands(self, conf_comm):
        if type(conf_comm) == str :
            self._write_line('conf t')
            output_sh = self.telnet.read_until(b"#", timeout=5).decode('utf-8')
            
            self._write_line(conf_comm)
            output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
            self._write_line('end')
            output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
            return output_sh
            
        elif type(conf_comm) == list :
            output_sh = ''
            self._write_line('conf t')
            for one_comm in conf_comm:
                self._write_line(one_comm)
                output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
            self._write_line('end')    
            output_sh = output_sh + self.telnet.read_until(b">", timeout=5).decode('utf-8')
            return output_sh
        

r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}


if __name__ == '__main__':
    r1 = CiscoTelnet(**r1_params)
    #print(r1.send_show_command("sh ip int br", parse=True))
    print(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))
