# -*- coding: utf-8 -*-
"""
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.
"""

ospf_route = "      10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"

x = ospf_route.split(",")
q = x[0].split()
q = q + x[1].split()
q = q + x[2].split()

a = {"Prefix" : q[0],
     "AD/Metric" : q[1].split('[')[1].split(']')[0],
     "Next-Hop" : q[3],
     "Last update" : q[4],
     "Outbound Interface" : q[5]}

result =  '''Prefix			{0:28}
AD/Metric		{1:28}
Next-Hop		{2:28}
Last update		{3:28}
Outbound Interface	{4:28}'''

print(result.format(str(a["Prefix"]), str(a["AD/Metric"]), str(a["Next-Hop"]), str(a["Last update"]), str(a["Outbound Interface"])))
#print("Prefix {0:28}".format(a["Prefix"]))
#print("AD/Metric {0:28}".format(a["AD/Metric"]))
