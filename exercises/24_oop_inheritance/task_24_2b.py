# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
from netmiko.cisco.cisco_ios import CiscoIosBase

device_params = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}
class ErrorInCommand(Exception):
    pass

class MyNetmiko(CiscoIosBase):
    def send_command(self, command, *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        if 'Invalid input' in command_output:
            raise ErrorInCommand('Ошибка в команде {}'.format(command))
        return command_output

    def say_hello(self):
        print('Hello from', self.ip)

if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)

    try:
        r1.send_command('sh ip br', strip_command = False)
    except ErrorInCommand as e:
        print('error', e)
