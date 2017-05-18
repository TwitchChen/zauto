#coding: utf-8

from flask import jsonify

"""
@file: zbx_delete_maintenance.py
@time: 2017/5/18 
@author: chenfan
"""

class zbx_delete_main:

    def __init__(self,zapi):
        self.zapi = zapi

    def host_interface_get(self, interface):
        response = self.zapi.host.get(
            output="extend",
            filter={'ip': interface}
        )
        return response

    def get_maintenance(self,hostid):
        response = self.zapi.maintenance.get(
            output='hosts',
            selectHosts='hostids',
            hostids=hostid
        )
        return response

    def delete_maintenance(self, mid):
        response = self.zapi.maintenance.delete(
            mid
        )
        if len(response["maintenanceids"]) != 0:
            return jsonify({"msg": "delete maintenance success", "status_code": 200}), 200
        else:
            return jsonify({"msg": "delete maintenance fail", "status_code": 500}), 500