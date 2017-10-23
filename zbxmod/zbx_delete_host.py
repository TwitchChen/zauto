#coding: utf-8

from flask import jsonify

"""
@file: zbx_delete_host.py
@time: 2017/5/18 
@author: chenfan
"""

class zbx_del_hosts:
    def __init__(self,zapi):
        self.zapi = zapi

    def host_interface_get(self, interface):
        response = self.zapi.host.get(
            output="extend",
            filter={'ip': interface}
        )
        return response

    def host_delete(self, hostid):
        response = self.zapi.host.delete(
            hostid
        )
        return response

    def host_exist(self, hostid):
        response = self.zapi.host.exists(
            hostid=hostid
        )
        return response

    def hostdelete(self, interface):
        response = self.host_interface_get(interface)
        hostid = []
        if response:
            for i in range(len(response)):
                hostid.append(response[i]['hostid'])
                self.host_delete(hostid[i])
            return jsonify({"msg":"delete hosts success", "status_code":200}),200
        else:
            return jsonify({"msg": "host does not exists", "status_code": 404}), 404