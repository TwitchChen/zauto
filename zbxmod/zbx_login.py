#coding: utf-8
from pyzabbix import ZabbixAPI
"""
@file: zbx_login.py
@time: 2017/5/17 
@author: chenfan
"""

def login(url,user,pwd):
    zapi = ZabbixAPI(url)
    zapi.login(user=user,password=pwd)
    return zapi
if __name__ == "__main__":
    url = "http://172.26.4.36"
    user = "chenfan"
    pwd = "123456"
    zapi = login(url,user,pwd)
    def hostexist(interface, hostname):
        ip_response = zapi.hostinterface.get(
            output="extend",
            filter={'ip': interface}
        )
        name_response=zapi.host.get(
            output="extend",
            filter={'host': hostname}
        )
        if ip_response and name_response:
            return True
        else:
            return False