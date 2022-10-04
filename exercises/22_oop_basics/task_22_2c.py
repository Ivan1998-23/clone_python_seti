# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
from scrapli.driver.core import IOSXEDriver
from scrapli.exceptions import ScrapliException
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
            
            
    def send_config_commands(self, conf_comm, strict=True ):
        def set_error(output_sh, one_comm):
            if 'Invalid input detected' in output_sh:   
                print('При выполнении команды "{0}" на устройстве {1}'.format(one_comm, self.ip),
                "возникла ошибка --> Invalid input detected at '^' marker.")
                return ValueError
            elif 'Incomplete command' in output_sh:   
                print('При выполнении команды "{0}" на устройстве {1}'.format(one_comm, self.ip),
                "возникла ошибка --> Incomplete command.")
                return ValueError
            elif 'Ambiguous command' in output_sh:   
                print('При выполнении команды "{0}" на устройстве {1}'.format(one_comm, self.ip),
                "возникла ошибка --> Ambiguous command.")
                return ValueError
        
        if strict == False:
            if type(conf_comm) == str :
                output_sh = ''
                self._write_line('conf t')
                output_sh = self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                
                self._write_line(conf_comm)
                output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                set_error(output_sh,conf_comm)
                self._write_line('end')
                output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                return output_sh
                
            elif type(conf_comm) == list :
                output_sh = ''
                self._write_line('conf t')
                for one_comm in conf_comm:
                    self._write_line(one_comm)
                    output = self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                    set_error(output_sh, one_comm)
                    output_sh = output_sh + output
                self._write_line('end')    
                output_sh = output_sh + self.telnet.read_until(b">", timeout=5).decode('utf-8')
                return output_sh
        else:
            if type(conf_comm) == str :
                output_sh = ''
                self._write_line('conf t')
                output_sh = self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                
                self._write_line(conf_comm)
                output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                set_error(output_sh, conf_comm)
                self._write_line('end')
                output_sh = output_sh + self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                return output_sh
                
            elif type(conf_comm) == list :
                output_sh = ''
                log =True
                self._write_line('conf t')
                for one_comm in conf_comm:
                    self._write_line(one_comm)
                    output = self.telnet.read_until(b"#", timeout=5).decode('utf-8')
                    if set_error(output, one_comm) == ValueError:
                        log = False
                        #raise ValueError("При выполнении команды возникла ошибка")
                        break
                if log:
                    output_sh = output_sh + output
                    self._write_line('end')    
                    output_sh = output_sh + self.telnet.read_until(b">", timeout=5).decode('utf-8')
                    return output_sh




r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
correct_commands = ['logging buffered 20010', 'ip http server']
commands = commands_with_errors+correct_commands
# не доделал. На False работает а на T
if __name__ == '__main__':
    r1 = CiscoTelnet(**r1_params)
    #print(r1.send_show_command("sh ip int br", parse=True))
    #print(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))
    print(r1.send_config_commands(commands, strict=True))
