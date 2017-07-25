#coding: utf-8
import time
from flask import jsonify
"""
@file: zbx_add_maintenance.py
@time: 2017/5/18 
@author: chenfan
"""

class zbx_add_main:

    def __init__(self,zapi):
        self.zapi = zapi

    def host_interface_get(self, interface):
        response = self.zapi.host.get(
            output="extend",
            filter={'ip': interface}
        )
        return response

    def add_maintenance(self,hostid):
        active_time = int(time.time())
        util_time = active_time + 864000  # 默认一次性维护10天
        mname = 'cmdb' + str(active_time)
        response = self.zapi.maintenance.create(
            {
                "name": mname,
                "active_since": active_time,
                "active_till": util_time,
                "hostids": [hostid],
                "timeperiods": [
                    {
                        "timeperiod_type": 0,
                        "period": 864000
                    }
                ],
            })
        if len(response["maintenanceids"]) != 0:
            return jsonify({"msg":"maintenance create success","status_code":200}),200
        else:
            return jsonify({"msg":"maintenance create fali","status_code":500}),500
