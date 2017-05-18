#-*- coding: UTF-8 -*-

"""
@file: zbx_add_hosts.py
@time: 2017/5/17
@author: chenfan
"""

class zbx_add_hosts:
    def __init__(self,zapi):
        self.zapi = zapi
    
    def group_exist(self,groupname):
        info = self.zapi.hostgroup.get(
            output="extend",
            filter={'name':"%s"%(groupname)}
        )
        if info:
            result = True
        else:
            result = False 
        return result
    
    def group_create(self,groupname):
        result = self.zapi.hostgroup.create(
            name = "%s"%(groupname)
        )
        group_id = result['groupids'][0]
        return group_id

    def screen_exist(self,name):
        result = self.zapi.screen.get(
            output="extend",
            filter={'name':'%s'%(name)}
        )
        #screen_id = result[0]['screenid']
        if result:
            return True
        else:
            return False

    def get_groupid(self,groupname):
        group_info = self.zapi.hostgroup.get(
            output="extend",
            filter={'name':'%s'%(groupname)}
        )
        #print group_info
        group_id = group_info[0]['groupid']
        return group_id

    def get_templateid(self,templatename):
        tempalte_info = self.zapi.template.get(
            output="templateid",
            filter={'name':'%s'%(templatename)}
        )
        templateid = tempalte_info[0]['templateid']
        return templateid
    
    def template_exist(self,templatename):
        info = self.zapi.template.get(
            output="extend",
            filter={'name':"%s"%(templatename)}
        )
        if info:
            result = True
        else:
            result = False
        return result
    
    def get_template_name(self,ops_name):
        template_name = ops_name + " " + "system base template"
        return template_name

    def group_template_id(self,pro_name,template_name):
        group_id_list = []
        template_id = None
        try:
            for i in range(len(pro_name)):
                if self.group_exist(pro_name[i]):
                    group_id = self.get_groupid(pro_name[i])
                else :
                    group_id = self.group_create(pro_name[i])
                group_id_list.append({"groupid":group_id})
         #   print group_id_list  
        except IndexError:
            print('indexerror,please check product name list!')
            
        try:
            template_id = self.get_templateid(template_name)
        except IndexError:
            print('indexerror,please check template name list!')
        return group_id_list,template_id

    def hostexist(self, interface, hostname):
        ip_response = self.zapi.hostinterface.get(
            output="extend",
            filter={'ip': interface}
        )
        name_response = self.zapi.host.get(
            output="extend",
            filter={'host': hostname}
        )
        if ip_response and name_response:
            return True
        else:
            return False

    def zabbix_add_host(self,hostname,interface,dev_name,templateid,groupid):
        if self.hostexist(interface,hostname) == False :
            response = self.zapi.host.create(
            {
                "host": hostname,
                "groups": groupid,
                "templates": templateid, 
                "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": interface,
                    "dns": "",
                    "port": "10050"
                }
                ],
                "macros": [
                {
                    "macro": "{$DEVOPS}",
                    "value": dev_name
                }
                ]
            })
            if response['hostids'] :
                return 'create host success!',200
            else :
                return 'add host fail!',200
        else :
            return '%s'%(self.hostexist(interface,hostname)),200




